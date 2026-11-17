//! Domain-neutral PNP tree evaluation. Domains supply facts and action results;
//! traversal, ancestor fallback and candidate ordering have one implementation.

use crate::pnp_core::pkm_alloc::{AllocError, String as PkmString, Vec as PkmVec};
use crate::pnp_core::strutil::join_path;

/// A compiled rule. Priority inheritance is resolved by domain ingestion.
pub trait Node: Sized {
    /// Stable attribution component.
    fn name(&self) -> &str;
    /// Effective priority.
    fn priority(&self) -> i64;
    /// Nested exceptions.
    fn children(&self) -> &[Self];
    /// Whether this node can speak for an abstaining descendant.
    fn has_direct_verdict(&self) -> bool;
}

/// An observable step; domains may collect explanations without side effects.
#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub enum Step {
    /// A matching child replaced this node's region.
    Shadowed,
    /// No child matched; this node's actions are resolved.
    Triggered,
    /// This ancestor speaks for an abstaining descendant, once per evaluation.
    Fallback,
}

/// Facts and action semantics belonging to one policy domain.
pub trait Domain<R: Node> {
    /// A complete decision. Distinct equally ranked decisions conflict.
    type Verdict: Copy + Eq;
    /// Reads the immutable domain snapshot, including enabled state.
    fn matches(&mut self, rule: &R) -> bool;
    /// Resolves actions and collects domain effects. `None` abstains.
    fn resolve(&mut self, rule: &R, path: &str) -> Result<Option<Self::Verdict>, AllocError>;
    /// Equal-priority strictness, higher first.
    fn strictness(&self, verdict: Self::Verdict) -> u8;
    /// Optional explanation hook. Does not influence the result.
    fn observe(&mut self, _rule: &R, _path: &str, _step: Step) -> Result<(), AllocError> {
        Ok(())
    }
}

/// A speaker and its complete decision, before collation.
#[derive(Debug)]
pub struct Candidate<V> {
    /// Domain decision.
    pub verdict: V,
    /// Effective priority of the speaker, not the abstaining descendant.
    pub priority: i64,
    /// Full speaker path.
    pub rule: PkmString,
}

/// Collation without imposing a domain's backstop or effects.
#[derive(Debug)]
pub struct Selection<V> {
    /// Every candidate, retained for diagnosis.
    pub candidates: PkmVec<Candidate<V>>,
    /// Index of the top candidate, or no candidate (domain backstop).
    pub winner: Option<usize>,
    /// Different decisions tied at the winning priority and strictness.
    /// A caller must refuse this result rather than use traversal order.
    pub conflict: bool,
}

struct Frame<'a, R> {
    rule: &'a R,
    path: PkmString,
    next: usize,
    any_child: bool,
}

/// Evaluates a forest with bounded-by-input heap traversal, never recursion.
pub fn evaluate<R: Node, D: Domain<R>>(
    roots: &[R],
    domain: &mut D,
) -> Result<Selection<D::Verdict>, AllocError> {
    let mut candidates = PkmVec::new();
    let mut spoken: PkmVec<*const R> = PkmVec::new();
    for root in roots {
        if !domain.matches(root) {
            continue;
        }
        let mut stack = PkmVec::new();
        stack.push(Frame {
            rule: root,
            path: join_path("", root.name())?,
            next: 0,
            any_child: false,
        })?;
        while let Some(top) = stack.last_mut() {
            if let Some(child) = top.rule.children().get(top.next) {
                top.next += 1;
                if domain.matches(child) {
                    top.any_child = true;
                    let path = join_path(top.path.as_str(), child.name())?;
                    stack.push(Frame {
                        rule: child,
                        path,
                        next: 0,
                        any_child: false,
                    })?;
                }
                continue;
            }
            let Some(done) = stack.pop() else { break };
            if done.any_child {
                domain.observe(done.rule, done.path.as_str(), Step::Shadowed)?;
                continue;
            }
            domain.observe(done.rule, done.path.as_str(), Step::Triggered)?;
            if let Some(verdict) = domain.resolve(done.rule, done.path.as_str())? {
                candidates.push(Candidate {
                    verdict,
                    priority: done.rule.priority(),
                    rule: done.path,
                })?;
                continue;
            }
            let Some(speaker) = stack.iter().rev().find(|f| f.rule.has_direct_verdict()) else {
                continue;
            };
            if spoken.iter().any(|p| core::ptr::eq(*p, speaker.rule)) {
                continue;
            }
            spoken.push(speaker.rule as *const R)?;
            domain.observe(speaker.rule, speaker.path.as_str(), Step::Fallback)?;
            if let Some(verdict) = domain.resolve(speaker.rule, speaker.path.as_str())? {
                candidates.push(Candidate {
                    verdict,
                    priority: speaker.rule.priority(),
                    rule: join_path("", speaker.path.as_str())?,
                })?;
            }
        }
    }
    let mut winner: Option<usize> = None;
    for (i, candidate) in candidates.iter().enumerate() {
        if winner.map_or(true, |w| {
            let current = &candidates[w];
            candidate.priority > current.priority
                || (candidate.priority == current.priority
                    && domain.strictness(candidate.verdict) > domain.strictness(current.verdict))
        }) {
            winner = Some(i);
        }
    }
    let conflict = winner.is_some_and(|w| {
        let top = &candidates[w];
        candidates.iter().any(|c| {
            c.priority == top.priority
                && domain.strictness(c.verdict) == domain.strictness(top.verdict)
                && c.verdict != top.verdict
        })
    });
    Ok(Selection {
        candidates,
        winner,
        conflict,
    })
}
