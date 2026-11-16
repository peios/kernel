mod common;
use common::*;
use kacs_core::advisory::*;
use kacs_core::*;

fn descriptor(owner: &[u8], aces: &[Vec<u8>]) -> Vec<u8> {
    let mut bytes = vec![0; 20];
    bytes[0] = 1;
    bytes[2..4].copy_from_slice(&(SE_SELF_RELATIVE | SE_DACL_PRESENT).to_le_bytes());
    bytes[4..8].copy_from_slice(&20u32.to_le_bytes());
    bytes.extend_from_slice(owner);
    let offset = bytes.len() as u32;
    bytes[16..20].copy_from_slice(&offset.to_le_bytes());
    bytes.extend_from_slice(&acl_bytes(aces));
    bytes
}

fn connect() -> GenericMapping {
    GenericMapping {
        read: 1,
        write: 0,
        execute: 1,
        all: 1,
    }
}

fn attribute(name: &str) -> Vec<u8> {
    let mut bytes = vec![0xf9];
    let value: Vec<_> = name.encode_utf16().flat_map(u16::to_le_bytes).collect();
    bytes.extend_from_slice(&(value.len() as u32).to_le_bytes());
    bytes.extend(value);
    bytes
}

#[test]
fn missing_groups_cannot_skip_a_deny_before_a_user_allow() {
    let user = sid_bytes([0, 0, 0, 0, 0, 5], &[21, 1000]);
    let blocked = sid_bytes([0, 0, 0, 0, 0, 5], &[21, 1001]);
    let bytes = descriptor(
        &user,
        &[
            basic_ace(ACCESS_DENIED_ACE_TYPE, 0, 1, &blocked),
            basic_ace(ACCESS_ALLOWED_ACE_TYPE, 0, 1, &user),
        ],
    );
    let sd = SecurityDescriptor::parse(&bytes).unwrap();
    let mut subject = SuppliedSubject {
        user: Some(parse_sid(&user)),
        ..Default::default()
    };
    let check = |subject: &SuppliedSubject<'_>| {
        access_check_subject(&sd, subject, 1, &connect(), None, 0).unwrap()
    };
    assert_eq!(check(&subject).decision, AdvisoryDecision::MissingContext);
    subject.groups = Some(&[]);
    assert_eq!(check(&subject).decision, AdvisoryDecision::Granted);
    let groups = [SidAndAttributes {
        sid: parse_sid(&blocked),
        attributes: SE_GROUP_ENABLED,
    }];
    subject.groups = Some(&groups);
    assert_eq!(check(&subject).decision, AdvisoryDecision::Denied);
}

#[test]
fn filtered_omission_is_unknown_but_confirmed_absence_is_usable() {
    let user = sid_bytes([0, 0, 0, 0, 0, 5], &[21, 1000]);
    let mut tokens = attribute("Department");
    tokens.push(0x8d); // Not_Exists
    let bytes = descriptor(
        &user,
        &[callback_ace(
            ACCESS_ALLOWED_CALLBACK_ACE_TYPE,
            0,
            1,
            &user,
            &expr(&tokens),
        )],
    );
    let sd = SecurityDescriptor::parse(&bytes).unwrap();
    let mut subject = SuppliedSubject {
        user: Some(parse_sid(&user)),
        groups: Some(&[]),
        ..Default::default()
    };
    let check = |subject: &SuppliedSubject<'_>| {
        access_check_subject(&sd, subject, 1, &connect(), None, 0).unwrap()
    };
    let result = check(&subject);
    assert_eq!(result.decision, AdvisoryDecision::MissingContext);
    assert_eq!(result.missing, MISSING_USER_CLAIMS);
    assert_eq!(result.granted, 0);
    subject.user_claims.absent = &["department"];
    assert_eq!(check(&subject).decision, AdvisoryDecision::Granted);
    subject.user_claims.absent = &[];
    subject.user_claims.complete = true;
    assert_eq!(check(&subject).decision, AdvisoryDecision::Granted);
    let claims = [ClaimAttribute::new(
        "department",
        0,
        vec![ClaimValue::String("household".into())],
    )];
    subject.user_claims.values = &claims;
    assert_eq!(check(&subject).decision, AdvisoryDecision::Denied);
    subject.user_claims.complete = false;
    assert_eq!(check(&subject).decision, AdvisoryDecision::Denied);
}

#[test]
fn group_policies_do_not_need_claims_and_known_inputs_match_existing_evaluation() {
    let user = sid_bytes([0, 0, 0, 0, 0, 5], &[21, 1000]);
    let group = sid_bytes([0, 0, 0, 0, 0, 5], &[21, 2000]);
    let bytes = descriptor(&user, &[basic_ace(ACCESS_ALLOWED_ACE_TYPE, 0, 1, &group)]);
    let sd = SecurityDescriptor::parse(&bytes).unwrap();
    for attributes in [SE_GROUP_ENABLED, SE_GROUP_USE_FOR_DENY_ONLY, 0] {
        let groups = [SidAndAttributes {
            sid: parse_sid(&group),
            attributes,
        }];
        let subject = SuppliedSubject {
            user: Some(parse_sid(&user)),
            groups: Some(&groups),
            ..Default::default()
        };
        let actual = access_check_subject(&sd, &subject, 1, &connect(), None, 0).unwrap();
        let token = TokenView {
            user: parse_sid(&user),
            groups: &groups,
            user_deny_only: false,
        };
        let expected = evaluate_dacl(&sd, &token, 1, &connect(), false).unwrap();
        assert_eq!(
            actual.decision == AdvisoryDecision::Granted,
            expected.success
        );
        assert_eq!(actual.granted, expected.granted);
    }
}

#[test]
fn contradictory_claim_knowledge_is_invalid_even_if_not_referenced() {
    let user = sid_bytes([0, 0, 0, 0, 0, 5], &[18]);
    let bytes = descriptor(&user, &[]);
    let sd = SecurityDescriptor::parse(&bytes).unwrap();
    let claims = [ClaimAttribute::new(
        "Department",
        0,
        vec![ClaimValue::String("home".into())],
    )];
    let subject = SuppliedSubject {
        user_claims: ClaimKnowledge {
            values: &claims,
            absent: &["department"],
            complete: false,
        },
        ..Default::default()
    };
    assert!(access_check_subject(&sd, &subject, 1, &connect(), None, 0).is_err());
}

#[test]
fn execution_labels_require_context_instead_of_using_the_callers_integrity() {
    let user = sid_bytes([0, 0, 0, 0, 0, 5], &[18]);
    let label = sid_bytes([0, 0, 0, 0, 0, 16], &[12288]);
    let mut bytes = descriptor(&user, &[basic_ace(ACCESS_ALLOWED_ACE_TYPE, 0, 1, &user)]);
    let sacl_offset = bytes.len() as u32;
    bytes[2..4]
        .copy_from_slice(&(SE_SELF_RELATIVE | SE_DACL_PRESENT | SE_SACL_PRESENT).to_le_bytes());
    bytes[12..16].copy_from_slice(&sacl_offset.to_le_bytes());
    bytes.extend(acl_bytes(&[basic_ace(
        SYSTEM_MANDATORY_LABEL_ACE_TYPE,
        0,
        1,
        &label,
    )]));
    let sd = SecurityDescriptor::parse(&bytes).unwrap();
    let subject = SuppliedSubject {
        user: Some(parse_sid(&user)),
        groups: Some(&[]),
        ..Default::default()
    };
    let result = access_check_subject(&sd, &subject, 1, &connect(), None, 0).unwrap();
    assert_eq!(result.decision, AdvisoryDecision::MissingContext);
    assert_eq!(result.missing, MISSING_EXECUTION_CONTEXT);
    assert_eq!(result.granted, 0);
}

#[test]
fn object_ace_is_never_silently_promoted_to_a_global_grant() {
    let user = sid_bytes([0, 0, 0, 0, 0, 5], &[18]);
    let mut ace = vec![ACCESS_ALLOWED_OBJECT_ACE_TYPE, 0, 0, 0];
    ace.extend(1u32.to_le_bytes());
    ace.extend(ACE_OBJECT_TYPE_PRESENT.to_le_bytes());
    ace.extend([7; 16]);
    ace.extend(&user);
    let size = ace.len() as u16;
    ace[2..4].copy_from_slice(&size.to_le_bytes());
    let bytes = descriptor(&user, &[ace]);
    let sd = SecurityDescriptor::parse(&bytes).unwrap();
    let subject = SuppliedSubject {
        user: Some(parse_sid(&user)),
        groups: Some(&[]),
        ..Default::default()
    };
    assert_eq!(
        access_check_subject(&sd, &subject, 1, &connect(), None, 0)
            .unwrap()
            .missing,
        MISSING_OBJECT_TYPES
    );
    for (guid, expected) in [
        ([7; 16], AdvisoryDecision::Granted),
        ([8; 16], AdvisoryDecision::Denied),
    ] {
        let tree = ObjectTypeList::new(&[ObjectTypeNode { level: 0, guid }]).unwrap();
        assert_eq!(
            access_check_subject(&sd, &subject, 1, &connect(), Some(&tree), 0)
                .unwrap()
                .decision,
            expected
        );
    }
}

#[test]
fn absent_identity_is_unknown_when_a_relevant_ace_can_match_it() {
    let user = sid_bytes([0, 0, 0, 0, 0, 5], &[18]);
    let bytes = descriptor(&user, &[basic_ace(ACCESS_ALLOWED_ACE_TYPE, 0, 1, &user)]);
    let sd = SecurityDescriptor::parse(&bytes).unwrap();
    let subject = SuppliedSubject {
        groups: Some(&[]),
        ..Default::default()
    };
    assert_eq!(
        access_check_subject(&sd, &subject, 1, &connect(), None, 0)
            .unwrap()
            .missing,
        MISSING_USER
    );
}

#[test]
fn requested_auditing_is_not_silently_discarded() {
    let user = sid_bytes([0, 0, 0, 0, 0, 5], &[18]);
    let mut bytes = descriptor(&user, &[basic_ace(ACCESS_ALLOWED_ACE_TYPE, 0, 1, &user)]);
    let offset = bytes.len() as u32;
    bytes[2..4]
        .copy_from_slice(&(SE_SELF_RELATIVE | SE_DACL_PRESENT | SE_SACL_PRESENT).to_le_bytes());
    bytes[12..16].copy_from_slice(&offset.to_le_bytes());
    bytes.extend(acl_bytes(&[basic_ace(
        SYSTEM_AUDIT_ACE_TYPE,
        0x40,
        1,
        &user,
    )]));
    let sd = SecurityDescriptor::parse(&bytes).unwrap();
    let subject = SuppliedSubject {
        user: Some(parse_sid(&user)),
        groups: Some(&[]),
        ..Default::default()
    };
    let result = access_check_subject(&sd, &subject, 1, &connect(), None, 0).unwrap();
    assert_eq!(result.decision, AdvisoryDecision::MissingContext);
    assert_eq!(result.missing, MISSING_AUDIT_CONTEXT);
    assert_eq!(result.granted, 0);
}
