//! Identity-based SD decisions without creating, adopting or inheriting a token.
//!
//! This entry point reuses the ordinary DACL/object/conditional evaluators. It
//! does not invent process privileges, integrity, confinement or a logon session.
//! Explicit execution labels and scoped policy therefore require context this
//! identity-only interface cannot supply. Existing full-token checks are unchanged.

use crate::ace::{
    AceKind, SYSTEM_MANDATORY_LABEL_ACE_TYPE, SYSTEM_PROCESS_TRUST_LABEL_ACE_TYPE,
    SYSTEM_SCOPED_POLICY_ID_ACE_TYPE,
};
use crate::claims::ClaimAttribute;
use crate::condition::{claim_names_equal, visit_conditional_dependencies, ConditionalContext};
use crate::dacl::{evaluate_dacl_result_list_with_context, evaluate_dacl_with_context};
use crate::error::{KacsError, KacsResult};
use crate::object_tree::ObjectTypeList;
use crate::sacl::extract_sacl_metadata;
use crate::security_descriptor::SecurityDescriptor;
use crate::sid::Sid;
use crate::token::{SidAndAttributes, TokenView};
use crate::{
    GenericMapping, ACCESS_SYSTEM_SECURITY, MAXIMUM_ALLOWED, READ_CONTROL, WRITE_DAC, WRITE_OWNER,
};

pub const MISSING_USER: u32 = 1;
pub const MISSING_GROUPS: u32 = 2;
pub const MISSING_USER_CLAIMS: u32 = 4;
pub const MISSING_DEVICE_GROUPS: u32 = 8;
pub const MISSING_DEVICE_CLAIMS: u32 = 16;
pub const MISSING_LOCAL_CLAIMS: u32 = 32;
pub const MISSING_SELF: u32 = 64;
pub const MISSING_OBJECT_TYPES: u32 = 128;
pub const MISSING_EXECUTION_CONTEXT: u32 = 256;
pub const MISSING_AUDIT_CONTEXT: u32 = 512;

/// Supplied claim values plus the names whose absence is known. A partial set
/// never turns an omitted name into a known absence.
#[derive(Clone, Copy, Debug, Default)]
pub struct ClaimKnowledge<'a> {
    pub values: &'a [ClaimAttribute],
    pub absent: &'a [&'a str],
    pub complete: bool,
}

impl ClaimKnowledge<'_> {
    fn validate(&self) -> KacsResult<()> {
        for (index, claim) in self.values.iter().enumerate() {
            if claim.name.is_empty()
                || claim.name.contains('\0')
                || self.values[..index]
                    .iter()
                    .any(|other| claim_names_equal(&other.name, &claim.name))
            {
                return Err(KacsError::InvalidAbiInput("advisory claim names"));
            }
        }
        for (index, name) in self.absent.iter().enumerate() {
            if name.is_empty()
                || name.contains('\0')
                || self.absent[..index]
                    .iter()
                    .any(|other| claim_names_equal(other, name))
                || self
                    .values
                    .iter()
                    .any(|claim| claim_names_equal(&claim.name, name))
            {
                return Err(KacsError::InvalidAbiInput("advisory absent claims"));
            }
        }
        Ok(())
    }
    fn knows(&self, name: &str) -> bool {
        self.complete
            || self
                .values
                .iter()
                .any(|claim| claim_names_equal(&claim.name, name))
            || self
                .absent
                .iter()
                .any(|absent| claim_names_equal(absent, name))
    }
}

/// None means unknown, independently of a supplied empty list. All identity
/// data is hypothetical: it conveys no kernel authority or impersonation right.
#[derive(Clone, Copy, Debug, Default)]
pub struct SuppliedSubject<'a> {
    pub user: Option<Sid<'a>>,
    pub groups: Option<&'a [SidAndAttributes<'a>]>,
    pub user_claims: ClaimKnowledge<'a>,
    pub device_groups: Option<&'a [SidAndAttributes<'a>]>,
    pub device_claims: ClaimKnowledge<'a>,
    pub local_claims: ClaimKnowledge<'a>,
    pub self_sid: Option<Sid<'a>>,
}

#[derive(Clone, Copy, Debug, Eq, PartialEq)]
pub enum AdvisoryDecision {
    Granted,
    Denied,
    MissingContext,
}

#[derive(Clone, Copy, Debug, Eq, PartialEq)]
pub struct AdvisoryResult {
    pub decision: AdvisoryDecision,
    /// Empty on missing context; no provisional grant may be used as admission.
    pub granted: u32,
    /// Missing input categories; deliberately does not name restricted claims.
    pub missing: u32,
}

/// Evaluate a supplied identity against an SD. Missing-context detection is
/// conservative: even an irrelevant conditional branch may require more data.
/// Object-list mode returns the selected node; no list means ordinary root
/// access and refuses GUID-scoped ACEs rather than treating them as global.
pub fn access_check_subject(
    sd: &SecurityDescriptor<'_>,
    subject: &SuppliedSubject<'_>,
    desired: u32,
    mapping: &GenericMapping,
    object_tree: Option<&ObjectTypeList>,
    node: usize,
) -> KacsResult<AdvisoryResult> {
    if sd.owner().is_none() {
        return Err(KacsError::MissingSecurityDescriptorOwner);
    }
    subject.user_claims.validate()?;
    subject.device_claims.validate()?;
    subject.local_claims.validate()?;
    let normalized = mapping.normalize_desired_access(desired)?;
    let relevant = if desired & MAXIMUM_ALLOWED != 0 {
        mapping.map_mask(crate::GENERIC_ALL)?
    } else {
        normalized.mapped
    };
    if object_tree.is_none() && node != 0 || object_tree.is_some_and(|tree| node >= tree.len()) {
        return Err(KacsError::InvalidAbiInput("advisory object node"));
    }
    let mut missing = 0;
    if relevant & (ACCESS_SYSTEM_SECURITY | WRITE_OWNER) != 0 {
        missing |= MISSING_EXECUTION_CONTEXT;
    }
    let metadata = extract_sacl_metadata(sd)?;
    if let Some(sacl) = sd.sacl() {
        for ace in sacl.entries() {
            let ace = ace?;
            if ace.ace_flags() & 0x08 == 0
                && matches!(
                    ace.ace_type(),
                    SYSTEM_MANDATORY_LABEL_ACE_TYPE
                        | SYSTEM_PROCESS_TRUST_LABEL_ACE_TYPE
                        | SYSTEM_SCOPED_POLICY_ID_ACE_TYPE
                )
            {
                missing |= MISSING_EXECUTION_CONTEXT;
            }
            if ace.ace_flags() & 0x08 == 0
                && matches!(
                    ace.ace_type(),
                    crate::ace::SYSTEM_AUDIT_ACE_TYPE
                        | crate::ace::SYSTEM_ALARM_ACE_TYPE
                        | crate::ace::SYSTEM_AUDIT_OBJECT_ACE_TYPE
                        | crate::ace::SYSTEM_ALARM_OBJECT_ACE_TYPE
                        | crate::ace::SYSTEM_AUDIT_CALLBACK_ACE_TYPE
                        | crate::ace::SYSTEM_ALARM_CALLBACK_ACE_TYPE
                        | crate::ace::SYSTEM_AUDIT_CALLBACK_OBJECT_ACE_TYPE
                        | crate::ace::SYSTEM_ALARM_CALLBACK_OBJECT_ACE_TYPE
                )
            {
                missing |= MISSING_AUDIT_CONTEXT;
            }
        }
    }
    if relevant & (READ_CONTROL | WRITE_DAC) != 0 {
        if subject.user.is_none() {
            missing |= MISSING_USER;
        }
        if subject.groups.is_none() {
            missing |= MISSING_GROUPS;
        }
    }
    if let Some(dacl) = sd.dacl() {
        for ace in dacl.entries() {
            let ace = ace?;
            if ace.ace_flags() & 0x08 != 0 {
                continue;
            }
            let (mask, sid, scoped, condition) = match ace.kind() {
                AceKind::SingleSid { mask, sid } => (mask, sid, false, None),
                AceKind::Object {
                    mask,
                    sid,
                    object_type,
                    ..
                } => (mask, sid, object_type.is_some(), None),
                AceKind::Callback {
                    mask,
                    sid,
                    application_data,
                } => (mask, sid, false, Some(application_data)),
                AceKind::CallbackObject {
                    mask,
                    sid,
                    object_type,
                    application_data,
                    ..
                } => (mask, sid, object_type.is_some(), Some(application_data)),
                _ => continue,
            };
            if mapping.map_mask(mask)? & relevant == 0 {
                continue;
            }
            if scoped && object_tree.is_none() {
                missing |= MISSING_OBJECT_TYPES;
            }
            if subject.user.is_none() {
                missing |= MISSING_USER;
            }
            if subject.user != Some(sid) && subject.groups.is_none() {
                missing |= MISSING_GROUPS;
            }
            if sid.identifier_authority() == [0, 0, 0, 0, 0, 5]
                && sid.sub_authority_count() == 1
                && sid.sub_authority(0) == Some(10)
                && subject.self_sid.is_none()
            {
                missing |= MISSING_SELF;
            }
            if let Some(condition) = condition {
                let valid = visit_conditional_dependencies(condition, |opcode, name| {
                    let unknown = match opcode {
                        0xf8 => !subject.local_claims.knows(name.unwrap_or("")),
                        0xf9 => !subject.user_claims.knows(name.unwrap_or("")),
                        0xfb => !subject.device_claims.knows(name.unwrap_or("")),
                        _ => false,
                    };
                    if unknown {
                        missing |= match opcode {
                            0xf8 => MISSING_LOCAL_CLAIMS,
                            0xf9 => MISSING_USER_CLAIMS,
                            _ => MISSING_DEVICE_CLAIMS,
                        };
                    }
                    if matches!(opcode, 0x89 | 0x8b | 0x90 | 0x92) && subject.groups.is_none() {
                        missing |= MISSING_GROUPS;
                    }
                    if matches!(opcode, 0x8a | 0x8c | 0x91 | 0x93)
                        && subject.device_groups.is_none()
                    {
                        missing |= MISSING_DEVICE_GROUPS;
                    }
                });
                if !valid {
                    return Err(KacsError::InvalidAbiInput("advisory condition"));
                }
            }
        }
    }
    if missing != 0 {
        return Ok(AdvisoryResult {
            decision: AdvisoryDecision::MissingContext,
            granted: 0,
            missing,
        });
    }
    // The parser requires a concrete TokenView. Its placeholder user can only
    // reach evaluation when no relevant ACE/owner operation observes the user.
    const UNUSED: &[u8] = &[1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0];
    let token = TokenView {
        user: subject.user.unwrap_or(Sid::parse(UNUSED)?),
        user_deny_only: false,
        groups: subject.groups.unwrap_or(&[]),
    };
    let context = ConditionalContext {
        self_sid: subject.self_sid,
        user_claims: subject.user_claims.values,
        device_claims: subject.device_claims.values,
        local_claims: subject.local_claims.values,
        resource_claims: metadata.resource_attributes.as_slice(),
        device_groups: subject.device_groups.unwrap_or(&[]),
        ..ConditionalContext::default()
    };
    let (granted, allowed) = if let Some(tree) = object_tree {
        let result = evaluate_dacl_result_list_with_context(
            sd, &token, desired, mapping, false, tree, &context,
        )?;
        (
            result.granted_list[node],
            result.status_list[node] == crate::dacl::AccessStatus::Ok,
        )
    } else {
        let result = evaluate_dacl_with_context(sd, &token, desired, mapping, false, &context)?;
        (result.granted, result.success)
    };
    Ok(AdvisoryResult {
        decision: if allowed {
            AdvisoryDecision::Granted
        } else {
            AdvisoryDecision::Denied
        },
        granted,
        missing: 0,
    })
}
