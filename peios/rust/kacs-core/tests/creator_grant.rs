//! The creator grant (PEI-1720): a creating open is granted what it asked
//! for in place of the normal DACL pass, and every other layer still refuses.

mod common;
use common::{acl_bytes, basic_ace, parse_sid, sid_bytes};
use kacs_core::{
    access_check, evaluate_security_descriptor, AccessCheckToken, CaapPolicy, CaapPolicyEntry,
    CaapRule, ConditionalContext, ConfinementTokenContext, EvaluateSecurityDescriptorInput,
    ImpersonationLevel, IntegrityLevel, PipContext, RestrictedTokenContext, SecurityDescriptor,
    Sid, SidAndAttributes, TokenPrivileges, TokenType, TokenView, ACCESS_ALLOWED_ACE_TYPE,
    ACCESS_SYSTEM_SECURITY, CREATOR_GRANT_INTENT, FILE_GENERIC_MAPPING, FILE_READ_DATA,
    FILE_WRITE_DATA, GENERIC_ALL, GENERIC_READ, MAXIMUM_ALLOWED, READ_CONTROL, SE_DACL_PRESENT,
    SE_GROUP_ENABLED, SE_SACL_PRESENT, SE_SECURITY_PRIVILEGE, SE_SELF_RELATIVE,
    SYSTEM_MANDATORY_LABEL_ACE_TYPE, SYSTEM_MANDATORY_LABEL_NO_WRITE_UP,
    TOKEN_MANDATORY_POLICY_NO_WRITE_UP, WRITE_DAC,
};

const SYSTEM_SCOPED_POLICY_ID_ACE_TYPE: u8 = 0x13;

fn sd_bytes(owner: &[u8], sacl: Option<&[u8]>, dacl: &[u8]) -> Vec<u8> {
    let control =
        SE_SELF_RELATIVE | SE_DACL_PRESENT | if sacl.is_some() { SE_SACL_PRESENT } else { 0 };
    let mut bytes = vec![0u8; 20];
    bytes[0] = 1;
    bytes[2..4].copy_from_slice(&control.to_le_bytes());

    let owner_offset = bytes.len() as u32;
    bytes[4..8].copy_from_slice(&owner_offset.to_le_bytes());
    bytes.extend_from_slice(owner);
    if let Some(sacl) = sacl {
        let sacl_offset = bytes.len() as u32;
        bytes[12..16].copy_from_slice(&sacl_offset.to_le_bytes());
        bytes.extend_from_slice(sacl);
    }
    let dacl_offset = bytes.len() as u32;
    bytes[16..20].copy_from_slice(&dacl_offset.to_le_bytes());
    bytes.extend_from_slice(dacl);
    bytes
}

fn primary_token<'a>(user: Sid<'a>) -> AccessCheckToken<'a> {
    AccessCheckToken {
        subject: TokenView {
            user,
            user_deny_only: false,
            groups: &[],
        },
        token_type: TokenType::Primary,
        impersonation_level: ImpersonationLevel::Impersonation,
        audit_policy: 0,
        privileges: TokenPrivileges::default(),
        integrity_level: IntegrityLevel::MEDIUM,
        mandatory_policy: TOKEN_MANDATORY_POLICY_NO_WRITE_UP,
        restricted: RestrictedTokenContext::default(),
        confinement: ConfinementTokenContext::default(),
    }
}

fn evaluate(sd: &SecurityDescriptor<'_>, token: &AccessCheckToken<'_>, desired: u32) -> u32 {
    evaluate_security_descriptor(EvaluateSecurityDescriptorInput {
        sd: Some(sd),
        token,
        pip: PipContext::default(),
        desired_access: desired,
        mapping: &FILE_GENERIC_MAPPING,
        object_tree: None,
        conditional_context: &ConditionalContext::default(),
        privilege_intent: CREATOR_GRANT_INTENT,
    })
    .expect("evaluation should succeed")
    .granted
}

fn owner() -> Vec<u8> {
    sid_bytes([0, 0, 0, 0, 0, 5], &[18])
}

fn user() -> Vec<u8> {
    sid_bytes([0, 0, 0, 0, 0, 5], &[21, 17201])
}

fn all_file_rights() -> u32 {
    FILE_GENERIC_MAPPING.map_mask(GENERIC_ALL).unwrap()
}

#[test]
fn empty_dacl_grants_the_creator_what_it_requested() {
    let owner = owner();
    let user = user();
    let sd_bytes = sd_bytes(&owner, None, &acl_bytes(&[]));
    let sd = SecurityDescriptor::parse(&sd_bytes).unwrap();
    let token = primary_token(parse_sid(&user));
    let desired = FILE_READ_DATA | FILE_WRITE_DATA | WRITE_DAC;

    assert_eq!(evaluate(&sd, &token, desired) & desired, desired);

    let without_grant = evaluate_security_descriptor(EvaluateSecurityDescriptorInput {
        sd: Some(&sd),
        token: &token,
        pip: PipContext::default(),
        desired_access: desired,
        mapping: &FILE_GENERIC_MAPPING,
        object_tree: None,
        conditional_context: &ConditionalContext::default(),
        privilege_intent: 0,
    })
    .unwrap();
    assert_eq!(without_grant.granted & desired, 0);
}

#[test]
fn generic_requests_are_granted_as_mapped() {
    let owner = owner();
    let user = user();
    let sd_bytes = sd_bytes(&owner, None, &acl_bytes(&[]));
    let sd = SecurityDescriptor::parse(&sd_bytes).unwrap();
    let token = primary_token(parse_sid(&user));
    let read = FILE_GENERIC_MAPPING.map_mask(GENERIC_READ).unwrap();

    assert_eq!(evaluate(&sd, &token, GENERIC_READ) & read, read);
}

#[test]
fn low_integrity_creator_under_high_no_write_up_label_cannot_write() {
    let owner = owner();
    let user = user();
    let high = sid_bytes([0, 0, 0, 0, 0, 16], &[12288]);
    let sacl = acl_bytes(&[basic_ace(
        SYSTEM_MANDATORY_LABEL_ACE_TYPE,
        0,
        SYSTEM_MANDATORY_LABEL_NO_WRITE_UP,
        &high,
    )]);
    let sd_bytes = sd_bytes(&owner, Some(&sacl), &acl_bytes(&[]));
    let sd = SecurityDescriptor::parse(&sd_bytes).unwrap();
    let mut token = primary_token(parse_sid(&user));
    token.integrity_level = IntegrityLevel::LOW;

    let granted = evaluate(&sd, &token, FILE_READ_DATA | FILE_WRITE_DATA);

    assert_eq!(granted & FILE_READ_DATA, FILE_READ_DATA);
    assert_eq!(granted & FILE_WRITE_DATA, 0);
}

#[test]
fn confinement_still_refuses_rights_its_sids_are_not_granted() {
    let owner = owner();
    let user = user();
    let confinement = sid_bytes([0, 0, 0, 0, 0, 15], &[2, 1720]);
    let dacl = acl_bytes(&[basic_ace(
        ACCESS_ALLOWED_ACE_TYPE,
        0,
        FILE_READ_DATA,
        &confinement,
    )]);
    let sd_bytes = sd_bytes(&owner, None, &dacl);
    let sd = SecurityDescriptor::parse(&sd_bytes).unwrap();
    let mut token = primary_token(parse_sid(&user));
    token.confinement = ConfinementTokenContext {
        confinement_sid: Some(parse_sid(&confinement)),
        confinement_capabilities: &[],
        confinement_exempt: false,
    };

    let granted = evaluate(&sd, &token, FILE_READ_DATA | FILE_WRITE_DATA);

    assert_eq!(granted & (FILE_READ_DATA | FILE_WRITE_DATA), FILE_READ_DATA);
}

#[test]
fn restricted_token_is_still_intersected() {
    let owner = owner();
    let user = user();
    let restricting = sid_bytes([0, 0, 0, 0, 0, 5], &[21, 17202]);
    let dacl = acl_bytes(&[basic_ace(
        ACCESS_ALLOWED_ACE_TYPE,
        0,
        FILE_READ_DATA,
        &restricting,
    )]);
    let sd_bytes = sd_bytes(&owner, None, &dacl);
    let sd = SecurityDescriptor::parse(&sd_bytes).unwrap();
    let restricted_sids = [SidAndAttributes {
        sid: parse_sid(&restricting),
        attributes: SE_GROUP_ENABLED,
    }];
    let mut token = primary_token(parse_sid(&user));
    token.restricted = RestrictedTokenContext {
        restricted_sids: &restricted_sids,
        restricted_device_groups: &[],
        write_restricted: false,
        privilege_granted: 0,
    };

    let granted = evaluate(&sd, &token, FILE_READ_DATA | FILE_WRITE_DATA);

    assert_eq!(granted & (FILE_READ_DATA | FILE_WRITE_DATA), FILE_READ_DATA);
}

#[test]
fn maximum_allowed_is_every_file_right_the_other_layers_allow() {
    let owner = owner();
    let user = user();
    let all = all_file_rights();
    let token = primary_token(parse_sid(&user));

    let open_sd_bytes = sd_bytes(&owner, None, &acl_bytes(&[]));
    let open_sd = SecurityDescriptor::parse(&open_sd_bytes).unwrap();
    assert_eq!(evaluate(&open_sd, &token, MAXIMUM_ALLOWED), all);

    let high = sid_bytes([0, 0, 0, 0, 0, 16], &[12288]);
    let sacl = acl_bytes(&[basic_ace(
        SYSTEM_MANDATORY_LABEL_ACE_TYPE,
        0,
        SYSTEM_MANDATORY_LABEL_NO_WRITE_UP,
        &high,
    )]);
    let labelled_sd_bytes = sd_bytes(&owner, Some(&sacl), &acl_bytes(&[]));
    let labelled_sd = SecurityDescriptor::parse(&labelled_sd_bytes).unwrap();
    let mut low = primary_token(parse_sid(&user));
    low.integrity_level = IntegrityLevel::LOW;
    let granted = evaluate(&labelled_sd, &low, MAXIMUM_ALLOWED);
    assert_eq!(granted & FILE_WRITE_DATA, 0);
    assert_eq!(granted & FILE_READ_DATA, FILE_READ_DATA);
    assert_eq!(granted & !all, 0);

    let confinement = sid_bytes([0, 0, 0, 0, 0, 15], &[2, 1721]);
    let confined_dacl = acl_bytes(&[basic_ace(
        ACCESS_ALLOWED_ACE_TYPE,
        0,
        FILE_READ_DATA | READ_CONTROL,
        &confinement,
    )]);
    let confined_sd_bytes = sd_bytes(&owner, None, &confined_dacl);
    let confined_sd = SecurityDescriptor::parse(&confined_sd_bytes).unwrap();
    let mut confined = primary_token(parse_sid(&user));
    confined.confinement = ConfinementTokenContext {
        confinement_sid: Some(parse_sid(&confinement)),
        confinement_capabilities: &[],
        confinement_exempt: false,
    };
    assert_eq!(
        evaluate(&confined_sd, &confined, MAXIMUM_ALLOWED),
        FILE_READ_DATA | READ_CONTROL
    );
}

#[test]
fn access_system_security_still_needs_the_privilege() {
    let owner = owner();
    let user = user();
    let sd_bytes = sd_bytes(&owner, None, &acl_bytes(&[]));
    let sd = SecurityDescriptor::parse(&sd_bytes).unwrap();
    let mut token = primary_token(parse_sid(&user));

    assert_eq!(
        evaluate(&sd, &token, FILE_READ_DATA | ACCESS_SYSTEM_SECURITY) & ACCESS_SYSTEM_SECURITY,
        0
    );
    assert_eq!(
        evaluate(&sd, &token, MAXIMUM_ALLOWED) & ACCESS_SYSTEM_SECURITY,
        0
    );

    token.privileges = TokenPrivileges {
        present: SE_SECURITY_PRIVILEGE,
        enabled: SE_SECURITY_PRIVILEGE,
        enabled_by_default: 0,
        used: 0,
    };
    assert_eq!(
        evaluate(&sd, &token, FILE_READ_DATA | ACCESS_SYSTEM_SECURITY),
        FILE_READ_DATA | ACCESS_SYSTEM_SECURITY
    );
}

#[test]
fn central_access_policy_still_narrows_the_grant() {
    let owner = owner();
    let user = user();
    let policy_sid = sid_bytes([0, 0, 0, 0, 0, 5], &[21, 17203]);
    let sacl = acl_bytes(&[basic_ace(
        SYSTEM_SCOPED_POLICY_ID_ACE_TYPE,
        0,
        0,
        &policy_sid,
    )]);
    let sd_bytes = sd_bytes(&owner, Some(&sacl), &acl_bytes(&[]));
    let sd = SecurityDescriptor::parse(&sd_bytes).unwrap();
    let token = primary_token(parse_sid(&user));
    let rule_dacl = acl_bytes(&[basic_ace(ACCESS_ALLOWED_ACE_TYPE, 0, FILE_READ_DATA, &user)]);
    let policies = [CaapPolicyEntry {
        sid: parse_sid(&policy_sid),
        policy: CaapPolicy {
            rules: vec![CaapRule {
                applies_to: None,
                effective_dacl: rule_dacl.as_slice(),
                effective_sacl: None,
                staged_dacl: None,
                staged_sacl: None,
            }]
            .into(),
        },
    }];

    let result = access_check(
        Some(&sd),
        &token,
        PipContext::default(),
        FILE_READ_DATA | FILE_WRITE_DATA,
        &FILE_GENERIC_MAPPING,
        None,
        &ConditionalContext::default(),
        None,
        CREATOR_GRANT_INTENT,
        &policies,
    )
    .expect("access check should succeed");

    assert!(!result.allowed);
    assert_eq!(
        result.granted & (FILE_READ_DATA | FILE_WRITE_DATA),
        FILE_READ_DATA
    );
}
