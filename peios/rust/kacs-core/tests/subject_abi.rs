mod common;
use common::*;
use kacs_core::advisory::*;
use kacs_core::subject_abi::*;
use kacs_core::*;

fn put(bytes: &mut [u8], at: usize, value: u32) {
    bytes[at..at + 4].copy_from_slice(&value.to_le_bytes());
}
fn user() -> Vec<u8> {
    sid_bytes([0, 0, 0, 0, 0, 5], &[21, 1000])
}
fn sd(sacl: &[Vec<u8>]) -> Vec<u8> {
    let user = user();
    let mut b = vec![0; 20];
    b[0] = 1;
    b[2..4].copy_from_slice(&(SE_SELF_RELATIVE | SE_DACL_PRESENT | SE_SACL_PRESENT).to_le_bytes());
    put(&mut b, 4, 20);
    b.extend(&user);
    let at = b.len() as u32;
    put(&mut b, 16, at);
    b.extend(acl_bytes(&[basic_ace(
        ACCESS_ALLOWED_ACE_TYPE,
        0,
        1,
        &user,
    )]));
    let at = b.len() as u32;
    put(&mut b, 12, at);
    b.extend(acl_bytes(sacl));
    b
}
fn wire(sections: [&[u8]; 13]) -> Vec<u8> {
    let mut b = vec![0; HEADER_BYTES];
    put(&mut b, 0, VERSION);
    put(&mut b, 12, 3);
    put(&mut b, 16, 1);
    put(&mut b, 20, 1);
    put(&mut b, 28, 1);
    put(&mut b, 32, 1);
    for (i, section) in sections.iter().enumerate() {
        if !section.is_empty() {
            let at = b.len() as u32;
            put(&mut b, 48 + i * 8, at);
            put(&mut b, 52 + i * 8, section.len() as u32);
            b.extend(*section);
        }
    }
    let len = b.len() as u32;
    put(&mut b, 4, len);
    b
}
fn check(b: &[u8], audit: bool) -> AdvisoryResult {
    let r = parse_subject_request(b).unwrap();
    check_subject(
        &r.sd,
        &r.subject(),
        r.desired,
        &r.mapping,
        r.tree.as_ref(),
        r.node,
        Some(audit),
    )
    .unwrap()
}
fn base(sd: &[u8], user: &[u8]) -> Vec<u8> {
    wire([
        sd,
        user,
        &[],
        &[],
        &[],
        &[],
        &[],
        &[],
        &[],
        &[],
        &[],
        &[],
        &[],
    ])
}

#[test]
fn known_empty_and_unknown_groups_are_distinct() {
    let mut b = base(&sd(&[]), &user());
    assert_eq!(check(&b, false).decision, AdvisoryDecision::Granted);
    put(&mut b, 12, 0);
    // This user-only ACE is still decidable without unrelated group facts.
    assert_eq!(check(&b, false).decision, AdvisoryDecision::Granted);
    let r = parse_subject_request(&b).unwrap();
    assert!(r.subject().groups.is_none());
    put(&mut b, 12, 3);
    let r = parse_subject_request(&b).unwrap();
    assert_eq!(r.subject().groups, Some(&[][..]));
}

#[test]
fn every_truncation_and_noncanonical_section_is_rejected() {
    let b = base(&sd(&[]), &user());
    for len in 0..b.len() {
        assert!(parse_subject_request(&b[..len]).is_err(), "len {len}");
    }
    for (at, value) in [
        (0, 2),
        (4, 0),
        (8, 2),
        (12, 4),
        (40, 8),
        (44, 1),
        (48, 0),
        (48, 153),
        (52, u32::MAX),
        (64, 1),
        (36, 1),
    ] {
        let mut bad = b.clone();
        put(&mut bad, at, value);
        assert!(parse_subject_request(&bad).is_err(), "at {at}");
    }
    let mut trailing = b.clone();
    trailing.push(0);
    let len = trailing.len() as u32;
    put(&mut trailing, 4, len);
    assert!(parse_subject_request(&trailing).is_err());
    let mut oversized = vec![0; MAX_BYTES + 1];
    put(&mut oversized, 0, VERSION);
    assert!(parse_subject_request(&oversized).is_err());
}

#[test]
fn duplicate_groups_unknown_attributes_and_unbounded_collections_are_invalid() {
    let user = user();
    let sd = sd(&[]);
    let mut group = (user.len() as u32).to_le_bytes().to_vec();
    group.extend(&user);
    group.extend(4u32.to_le_bytes());
    let build = |groups: &[u8]| {
        wire([
            &sd,
            &user,
            groups,
            &[],
            &[],
            &[],
            &[],
            &[],
            &[],
            &[],
            &[],
            &[],
            &[],
        ])
    };
    assert!(parse_subject_request(&build(&group)).is_ok());
    let mut duplicate = group.clone();
    duplicate.extend(&group);
    assert!(parse_subject_request(&build(&duplicate)).is_err());
    let len = group.len();
    put(&mut group, len - 4, 0x100);
    assert!(parse_subject_request(&build(&group)).is_err());
    // A section cannot secretly supply facts whose known bit is clear.
    let mut bad = build(&duplicate[..duplicate.len() / 2]);
    put(&mut bad, 12, 0);
    assert!(parse_subject_request(&bad).is_err());
}

#[test]
fn active_auditing_reuses_success_and_failure_sacl_matching() {
    for (desired, flag, expected) in [(1, 0x40, true), (3, 0x80, false)] {
        let sd = sd(&[basic_ace(SYSTEM_AUDIT_ACE_TYPE, flag, 3, &user())]);
        let mut b = base(&sd, &user());
        put(&mut b, 16, desired);
        let r = parse_subject_request(&b).unwrap();
        let result = check(&b, true);
        assert_eq!(result.decision == AdvisoryDecision::Granted, expected);
        let events = audit_subject(
            &r.sd,
            &r.subject(),
            r.desired,
            &r.mapping,
            None,
            0,
            result.granted,
            None,
        )
        .unwrap();
        assert_eq!(events.audit_events.len(), 1);
        assert_eq!(events.audit_events[0].success, expected);
        assert!(!events.audit_events[0].policy_forced);
        assert_eq!(check(&b, false), result);
    }
}

#[test]
fn audit_only_claim_dependencies_disappear_when_auditing_is_suppressed() {
    let utf16: Vec<u8> = "secret".encode_utf16().flat_map(u16::to_le_bytes).collect();
    let mut condition = vec![0xf9];
    condition.extend((utf16.len() as u32).to_le_bytes());
    condition.extend(utf16);
    condition.push(0x87); // Exists
    let sd = sd(&[callback_ace(
        SYSTEM_AUDIT_CALLBACK_ACE_TYPE,
        0x40,
        1,
        &user(),
        &expr(&condition),
    )]);
    let mut b = base(&sd, &user());
    assert_eq!(check(&b, true).missing, MISSING_USER_CLAIMS);
    assert_eq!(check(&b, false).decision, AdvisoryDecision::Granted);
    put(&mut b, 40, 1); // Known absent in a complete user-claim set.
    assert_eq!(check(&b, true).decision, AdvisoryDecision::Granted);
}

#[test]
fn suppression_never_bypasses_integrity_or_scoped_policy_labels() {
    let label = sid_bytes([0, 0, 0, 0, 0, 16], &[0x3000]);
    for ty in [
        SYSTEM_MANDATORY_LABEL_ACE_TYPE,
        SYSTEM_PROCESS_TRUST_LABEL_ACE_TYPE,
        SYSTEM_SCOPED_POLICY_ID_ACE_TYPE,
    ] {
        let sd = sd(&[basic_ace(ty, 0, 1, &label)]);
        let b = base(&sd, &user());
        for audit in [false, true] {
            assert_ne!(check(&b, audit).missing & MISSING_EXECUTION_CONTEXT, 0);
        }
    }
}

#[test]
fn repeated_offsets_cannot_expand_subject_or_resource_claims_without_bound() {
    let mut entry = vec![0; 8192];
    put(&mut entry, 0, 4112); // name
    entry[4..6].copy_from_slice(&3u16.to_le_bytes()); // UTF-16 string values
    put(&mut entry, 12, 1024);
    for i in 0..1024 {
        put(&mut entry, 16 + i * 4, 4116);
    }
    entry[4112] = b'x';
    put(&mut entry, 4116, 4120);
    for i in 0..2000 {
        entry[4120 + i * 2] = b'q';
    }
    // Individually valid typed data, but its aliased string offsets would
    // repeatedly allocate the same long value when fully decoded.
    kacs_core::claims::validate_claim_attribute_entry(&entry).unwrap();
    let resource_sd = sd(&[resource_attribute_ace(0, &entry)]);
    assert!(parse_subject_request(&base(&resource_sd, &user())).is_err());
    let plain_sd = sd(&[]);
    let user = user();
    let mut claims = (entry.len() as u32).to_le_bytes().to_vec();
    claims.extend(entry);
    let b = wire([
        &plain_sd,
        &user,
        &[],
        &[],
        &claims,
        &[],
        &[],
        &[],
        &[],
        &[],
        &[],
        &[],
        &[],
    ]);
    assert!(parse_subject_request(&b).is_err());
}
