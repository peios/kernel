//! The evaluation algorithm (ratified design, PEI-598):
//!
//! 1. Matching reads the immutable snapshot.
//! 2. Trigger set: a node triggers iff it and all ancestors match and no
//!    child matches (shadowing exists only within a lineage).
//! 3. Every triggered rule's side effects execute — priority never
//!    suppresses side effects. Reports dedup per rule and honor the
//!    reporting threshold. Prompts are issued; with no handler answer the
//!    fallback applies (v0 has no handler transport, so every prompt takes
//!    the unanswered path immediately).
//! 4. A triggered rule yielding no verdict walks up its own parentage to
//!    the first ancestor whose actions contain a direct verdict; that
//!    ancestor speaks for the region, executing its full action list once.
//! 5. Collation: highest priority wins; ties resolve strictest
//!    (DROP > REJECT > PASS). Attribution is the yielding rule's path.
//! 6. Nothing yielded anywhere: DROP, attributed to the backstop.
//!
//! Effects are computed here and applied by the glue after collation —
//! so a COUNT lands after this evaluation's own reads (temporal feedback:
//! the next packet sees it), and a REPORT can carry the verdict.

use crate::pnp_core::action::{Action, CountAmount, TagOp, Verdict, MAX_PROMPT_CHAIN};
use crate::pnp_core::machinery::{self, Domain, Node};
use crate::pnp_core::pkm_alloc::{AllocError, String as PkmString, TryClone, Vec as PkmVec};
use crate::pnp_core::rule::{Forest, MatchTrace, Rule};
use crate::pnp_core::snapshot::Snapshot;
use crate::pnp_core::strutil::str_to_pkm;

/// Evaluation-time configuration.
#[derive(Debug, Clone, Copy)]
pub struct EvalContext {
    /// `CurrentReportingLevel`: a REPORT fires when its level >= this.
    /// Absent from the registry = 1 (everything fires — quietness ships as
    /// a visible value); 6 silences everything.
    pub reporting_level: u8,
}

impl Default for EvalContext {
    fn default() -> Self {
        EvalContext { reporting_level: 1 }
    }
}

/// A side effect the caller must apply (side effects always execute for
/// every triggered rule; the core computes, the glue applies).
#[derive(Debug)]
pub enum Effect {
    /// Write flow-scoped state (no-op on untracked packets — glue's call).
    Tag {
        /// Tag name.
        name: PkmString,
        /// `name_hash(name)`: the store identity.
        hash: u64,
        /// Operation.
        op: TagOp,
    },
    /// Emit into a counter stream; the store increments every table the
    /// forest materialized for it.
    Count {
        /// Stream name.
        name: PkmString,
        /// `name_hash(name)`.
        hash: u64,
        /// Resolved amount (0 when the amount was `Length` and the packet
        /// has no length fact — the glue counts that as a no-op).
        amount: u64,
    },
    /// Emit an event, attributed to the rule.
    Report {
        /// Attribution path of the reporting rule.
        rule: PkmString,
        /// Severity (1..=5), already threshold-checked.
        level: u8,
    },
    /// A PROMPT was issued (observability; v0 has no handler transport, so
    /// the fallback path has already been taken).
    PromptIssued {
        /// Attribution path of the prompting rule.
        rule: PkmString,
        /// Handler name.
        handler: PkmString,
    },
}

/// One yielded verdict, before collation. Exposed so viewers can show every
/// speaker, not just the winner.
pub type VerdictCandidate = machinery::Candidate<Verdict>;

/// The result of judging one traversal against one forest.
#[derive(Debug)]
pub struct Evaluation {
    /// The layer's verdict for this traversal.
    pub verdict: Verdict,
    /// Attribution: the winning rule's path, or `backstop`.
    pub attributed_to: PkmString,
    /// Whether the backstop answered (nothing else yielded).
    pub backstop: bool,
    /// Side effects to apply.
    pub effects: PkmVec<Effect>,
    /// Every yielded verdict (winner included), for observability.
    pub candidates: PkmVec<VerdictCandidate>,
    /// When this evaluation's answer could next change on its own: the
    /// earliest flip of any live-time condition it consulted (epoch
    /// seconds, UTC), or `None` when none was consulted. The Flow layer's
    /// sentence expiry; meaningless for per-packet layers.
    pub expires_at: Option<i64>,
    /// Two candidates tied on priority and strictness with different
    /// verdicts — only possible in the interface layer, as `JOIN(a)`
    /// against `JOIN(b)`. The winner above is the first such candidate
    /// walked, which is no answer at all: the executor must refuse the
    /// generation rather than pick, and `candidates` names both rules.
    pub conflict: bool,
}

/// Judges one snapshot against one forest.
pub fn evaluate(
    forest: &Forest,
    snap: &Snapshot<'_>,
    ctx: &EvalContext,
) -> Result<Evaluation, AllocError> {
    let mut domain = PacketDomain {
        snap,
        ctx,
        effects: PkmVec::new(),
        trace: MatchTrace::default(),
    };
    let selected = machinery::evaluate(forest.roots.as_slice(), &mut domain)?;
    let (verdict, attributed_to) = match selected.winner {
        Some(w) => {
            let top = &selected.candidates[w];
            (top.verdict, top.rule.try_clone()?)
        }
        None => (forest.layer.backstop(), str_to_pkm("backstop")?),
    };
    Ok(Evaluation {
        verdict,
        attributed_to,
        backstop: selected.winner.is_none(),
        effects: domain.effects,
        candidates: selected.candidates,
        expires_at: domain.trace.expires_at,
        conflict: selected.conflict,
    })
}

impl Node for Rule {
    fn name(&self) -> &str {
        self.name.as_str()
    }
    fn priority(&self) -> i64 {
        self.priority
    }
    fn children(&self) -> &[Self] {
        self.children.as_slice()
    }
    fn has_direct_verdict(&self) -> bool {
        Rule::has_direct_verdict(self)
    }
}

struct PacketDomain<'s, 'p> {
    snap: &'s Snapshot<'p>,
    ctx: &'s EvalContext,
    effects: PkmVec<Effect>,
    trace: MatchTrace,
}
impl Domain<Rule> for PacketDomain<'_, '_> {
    type Verdict = Verdict;
    fn matches(&mut self, rule: &Rule) -> bool {
        rule.matches_traced(self.snap, &mut self.trace)
    }
    fn resolve(&mut self, rule: &Rule, path: &str) -> Result<Option<Verdict>, AllocError> {
        resolve_rule(rule, path, self.snap, self.ctx, &mut self.effects)
    }
    fn strictness(&self, verdict: Verdict) -> u8 {
        verdict.strictness()
    }
}

/// Resolves one rule's action list: pushes its side effects (report dedup
/// per rule; threshold applied) and returns its yielded verdict, if any.
/// Prompts take the unanswered path: issue the effect, apply the fallback.
fn resolve_rule(
    rule: &Rule,
    path: &str,
    snap: &Snapshot<'_>,
    ctx: &EvalContext,
    effects: &mut PkmVec<Effect>,
) -> Result<Option<Verdict>, AllocError> {
    let mut verdict: Option<Verdict> = None;
    let mut best_report: Option<u8> = None;
    for action in rule.actions.iter() {
        resolve_action(
            action,
            path,
            snap,
            effects,
            &mut verdict,
            &mut best_report,
            0,
        )?;
    }
    if let Some(level) = best_report {
        if level >= ctx.reporting_level {
            effects.push(Effect::Report {
                rule: str_to_pkm(path)?,
                level,
            })?;
        }
    }
    Ok(verdict)
}

fn resolve_action(
    action: &Action,
    path: &str,
    snap: &Snapshot<'_>,
    effects: &mut PkmVec<Effect>,
    verdict: &mut Option<Verdict>,
    best_report: &mut Option<u8>,
    depth: usize,
) -> Result<(), AllocError> {
    match action {
        Action::Null => {}
        // Ingestion lowers every JOIN to `Verdict::Join(index)`; one that
        // survived would be a bug, and abstaining is the harmless answer.
        Action::Join { .. } => {}
        Action::Verdict(v) => {
            *verdict = Some(match *verdict {
                Some(cur) => cur.strictest(*v),
                None => *v,
            });
        }
        Action::Tag { name, op } => effects.push(Effect::Tag {
            name: name.try_clone()?,
            hash: crate::pnp_core::hash::name_hash(name.as_str()),
            op: *op,
        })?,
        Action::Count { name, amount } => effects.push(Effect::Count {
            name: name.try_clone()?,
            hash: crate::pnp_core::hash::name_hash(name.as_str()),
            amount: match amount {
                CountAmount::Literal(v) => *v,
                CountAmount::Length => u64::from(snap.length.unwrap_or(0)),
            },
        })?,
        Action::Report { level } => {
            *best_report = Some(match *best_report {
                Some(cur) if cur >= *level => cur,
                _ => *level,
            });
        }
        Action::Prompt { handler, fallback } => {
            effects.push(Effect::PromptIssued {
                rule: str_to_pkm(path)?,
                handler: handler.try_clone()?,
            })?;
            // No handler transport in v0: the unanswered path, immediately.
            if depth < MAX_PROMPT_CHAIN {
                if let Some(inner) = fallback.action() {
                    resolve_action(inner, path, snap, effects, verdict, best_report, depth + 1)?;
                }
            }
        }
    }
    Ok(())
}
