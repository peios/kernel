//! Generic rights are mapped in every descriptor KACS stores (PEI-1720):
//! `map_acl_generic_rights` is what each write path stores.

mod common;
use common::{acl_bytes, basic_ace, sid_bytes};
use kacs_core::access_mask::IPC_GENERIC_MAPPING;
use kacs_core::{
    map_acl_generic_rights, Acl, ACCESS_ALLOWED_ACE_TYPE, ACCESS_DENIED_ACE_TYPE,
    CONTAINER_INHERIT_ACE, FILE_GENERIC_MAPPING, FILE_READ_DATA, GENERIC_ALL, GENERIC_READ,
    GENERIC_WRITE, INHERITED_ACE, INHERIT_ONLY_ACE, NO_PROPAGATE_INHERIT_ACE, OBJECT_INHERIT_ACE,
    SYSTEM_AUDIT_ACE_TYPE, SYSTEM_MANDATORY_LABEL_ACE_TYPE, SYSTEM_MANDATORY_LABEL_NO_WRITE_UP,
};

fn mapped(acl: &[u8], mapping: &kacs_core::GenericMapping) -> Option<Vec<u8>> {
    map_acl_generic_rights(Acl::parse(acl).unwrap(), mapping)
        .expect("mapping should succeed")
        .map(|bytes| bytes.as_slice().to_vec())
}

fn user() -> Vec<u8> {
    sid_bytes([0, 0, 0, 0, 0, 5], &[21, 17204])
}

#[test]
fn generic_all_on_a_file_ace_reads_back_mapped() {
    let user = user();
    let all = FILE_GENERIC_MAPPING.map_mask(GENERIC_ALL).unwrap();
    let acl = acl_bytes(&[basic_ace(ACCESS_ALLOWED_ACE_TYPE, 0, GENERIC_ALL, &user)]);

    let stored = mapped(&acl, &FILE_GENERIC_MAPPING).expect("GA has to be mapped");

    assert_eq!(
        stored,
        acl_bytes(&[basic_ace(ACCESS_ALLOWED_ACE_TYPE, 0, all, &user)])
    );
}

#[test]
fn applying_inheritable_ace_is_split_as_inheritance_splits_it() {
    let user = user();
    let read = FILE_GENERIC_MAPPING.map_mask(GENERIC_READ).unwrap();
    let flags = OBJECT_INHERIT_ACE | CONTAINER_INHERIT_ACE | INHERITED_ACE;
    let acl = acl_bytes(&[basic_ace(
        ACCESS_ALLOWED_ACE_TYPE,
        flags,
        GENERIC_READ | FILE_READ_DATA,
        &user,
    )]);

    let stored = mapped(&acl, &FILE_GENERIC_MAPPING).expect("GR has to be mapped");

    assert_eq!(
        stored,
        acl_bytes(&[
            basic_ace(
                ACCESS_ALLOWED_ACE_TYPE,
                INHERITED_ACE,
                read | FILE_READ_DATA,
                &user
            ),
            basic_ace(
                ACCESS_ALLOWED_ACE_TYPE,
                flags | INHERIT_ONLY_ACE,
                GENERIC_READ | FILE_READ_DATA,
                &user,
            ),
        ])
    );
}

#[test]
fn no_propagate_is_cleared_from_the_effective_ace_and_kept_on_the_rule() {
    let user = user();
    let write = FILE_GENERIC_MAPPING.map_mask(GENERIC_WRITE).unwrap();
    let flags = CONTAINER_INHERIT_ACE | NO_PROPAGATE_INHERIT_ACE;
    let acl = acl_bytes(&[basic_ace(
        ACCESS_DENIED_ACE_TYPE,
        flags,
        GENERIC_WRITE,
        &user,
    )]);

    let stored = mapped(&acl, &FILE_GENERIC_MAPPING).unwrap();

    assert_eq!(
        stored,
        acl_bytes(&[
            basic_ace(ACCESS_DENIED_ACE_TYPE, 0, write, &user),
            basic_ace(
                ACCESS_DENIED_ACE_TYPE,
                flags | INHERIT_ONLY_ACE,
                GENERIC_WRITE,
                &user
            ),
        ])
    );
}

#[test]
fn inherit_only_aces_are_stored_as_given() {
    let user = user();
    let inherit_only = basic_ace(
        ACCESS_ALLOWED_ACE_TYPE,
        OBJECT_INHERIT_ACE | INHERIT_ONLY_ACE,
        GENERIC_ALL,
        &user,
    );
    let all = FILE_GENERIC_MAPPING.map_mask(GENERIC_ALL).unwrap();

    assert_eq!(
        mapped(&acl_bytes(&[inherit_only.clone()]), &FILE_GENERIC_MAPPING),
        None
    );

    let acl = acl_bytes(&[
        inherit_only.clone(),
        basic_ace(ACCESS_ALLOWED_ACE_TYPE, 0, GENERIC_ALL, &user),
    ]);
    assert_eq!(
        mapped(&acl, &FILE_GENERIC_MAPPING).unwrap(),
        acl_bytes(&[
            inherit_only,
            basic_ace(ACCESS_ALLOWED_ACE_TYPE, 0, all, &user)
        ])
    );
}

#[test]
fn acl_without_generic_rights_is_left_to_the_caller_unchanged() {
    let user = user();
    let acl = acl_bytes(&[basic_ace(
        ACCESS_ALLOWED_ACE_TYPE,
        OBJECT_INHERIT_ACE,
        FILE_READ_DATA,
        &user,
    )]);

    assert_eq!(mapped(&acl, &FILE_GENERIC_MAPPING), None);
}

#[test]
fn audit_aces_are_mapped_and_mandatory_labels_are_not() {
    let user = user();
    let high = sid_bytes([0, 0, 0, 0, 0, 16], &[12288]);
    let label = basic_ace(
        SYSTEM_MANDATORY_LABEL_ACE_TYPE,
        0,
        SYSTEM_MANDATORY_LABEL_NO_WRITE_UP,
        &high,
    );
    let write = FILE_GENERIC_MAPPING.map_mask(GENERIC_WRITE).unwrap();
    let sacl = acl_bytes(&[
        label.clone(),
        basic_ace(SYSTEM_AUDIT_ACE_TYPE, 0x80, GENERIC_WRITE, &user),
    ]);

    assert_eq!(
        mapped(&sacl, &FILE_GENERIC_MAPPING).unwrap(),
        acl_bytes(&[label, basic_ace(SYSTEM_AUDIT_ACE_TYPE, 0x80, write, &user)])
    );
}

#[test]
fn other_object_types_map_through_their_own_mapping() {
    let user = user();
    let acl = acl_bytes(&[basic_ace(ACCESS_ALLOWED_ACE_TYPE, 0, GENERIC_ALL, &user)]);
    let ipc_all = IPC_GENERIC_MAPPING.map_mask(GENERIC_ALL).unwrap();
    assert_ne!(ipc_all, FILE_GENERIC_MAPPING.map_mask(GENERIC_ALL).unwrap());

    assert_eq!(
        mapped(&acl, &IPC_GENERIC_MAPPING).unwrap(),
        acl_bytes(&[basic_ace(ACCESS_ALLOWED_ACE_TYPE, 0, ipc_all, &user)])
    );
}
