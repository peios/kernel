//! Bounded supplied-subject wire request. Parse only the kernel-owned copy.
//! All integers are little endian; sections are packed in header order, with
//! zero offset/length for an empty section. No nested userspace pointers exist.

use crate::advisory::{ClaimKnowledge, SuppliedSubject};
use crate::claims::{parse_claim_attribute_entry, ClaimAttribute};
use crate::error::{KacsError, KacsResult};
use crate::object_tree::{ObjectTypeList, ObjectTypeNode};
use crate::pkm_alloc::Vec;
use crate::{GenericMapping, SecurityDescriptor, Sid, SidAndAttributes};

pub const VERSION: u32 = crate::peios_uapi::KACS_SUBJECT_VERSION;
pub const HEADER_BYTES: usize = crate::peios_uapi::KACS_SUBJECT_HEADER_BYTES as usize;
pub const MAX_BYTES: usize = crate::peios_uapi::KACS_SUBJECT_MAX_BYTES as usize;
pub const MAX_ITEMS: usize = crate::peios_uapi::KACS_SUBJECT_MAX_ITEMS as usize;
pub const NO_AUDIT: u32 = crate::peios_uapi::KACS_SUBJECT_NO_AUDIT;
const INVALID: KacsError = KacsError::InvalidAbiInput("supplied-subject request");

/// Parsed request borrowing only its owned ingress buffer. Collection storage
/// is fallible; known-empty groups differ from unknown groups.
pub struct SubjectRequest<'a> {
    pub flags: u32,
    pub desired: u32,
    pub mapping: GenericMapping,
    pub node: usize,
    pub sd: SecurityDescriptor<'a>,
    pub tree: Option<ObjectTypeList>,
    pub audit_context: Option<&'a [u8]>,
    user: Option<Sid<'a>>,
    groups: Option<Vec<SidAndAttributes<'a>>>,
    device_groups: Option<Vec<SidAndAttributes<'a>>>,
    claims: [Vec<ClaimAttribute>; 3],
    absent: [Vec<&'a str>; 3],
    coverage: u32,
    self_sid: Option<Sid<'a>>,
}

impl SubjectRequest<'_> {
    pub fn subject(&self) -> SuppliedSubject<'_> {
        let knowledge = |i: usize| ClaimKnowledge {
            values: &self.claims[i],
            absent: &self.absent[i],
            complete: self.coverage & (1 << i) != 0,
        };
        SuppliedSubject {
            user: self.user,
            groups: self.groups.as_deref(),
            device_groups: self.device_groups.as_deref(),
            user_claims: knowledge(0),
            device_claims: knowledge(1),
            local_claims: knowledge(2),
            self_sid: self.self_sid,
        }
    }
}

fn u32_at(bytes: &[u8], at: usize) -> KacsResult<u32> {
    let raw = bytes
        .get(at..at.checked_add(4).ok_or(INVALID)?)
        .ok_or(INVALID)?;
    Ok(u32::from_le_bytes(raw.try_into().map_err(|_| INVALID)?))
}

fn take<'a>(bytes: &'a [u8], cursor: &mut usize, len: usize) -> KacsResult<&'a [u8]> {
    let end = cursor.checked_add(len).ok_or(INVALID)?;
    let value = bytes.get(*cursor..end).ok_or(INVALID)?;
    *cursor = end;
    Ok(value)
}

fn entries(bytes: &[u8], mut visit: impl FnMut(&[u8]) -> KacsResult<()>) -> KacsResult<()> {
    let mut cursor = 0;
    let mut count = 0;
    while cursor < bytes.len() {
        count += 1;
        if count > MAX_ITEMS {
            return Err(INVALID);
        }
        let len = u32_at(bytes, cursor)? as usize;
        cursor += 4;
        if len == 0 {
            return Err(INVALID);
        }
        visit(take(bytes, &mut cursor, len)?)?;
    }
    Ok(())
}

fn optional_sid(bytes: &[u8]) -> KacsResult<Option<Sid<'_>>> {
    if bytes.is_empty() {
        Ok(None)
    } else {
        Sid::parse(bytes).map(Some)
    }
}

fn groups(bytes: &[u8], known: bool) -> KacsResult<Option<Vec<SidAndAttributes<'_>>>> {
    if !known {
        return if bytes.is_empty() {
            Ok(None)
        } else {
            Err(INVALID)
        };
    }
    let mut out: Vec<SidAndAttributes<'_>> = Vec::new();
    let mut cursor = 0;
    while cursor < bytes.len() {
        if out.len() >= MAX_ITEMS {
            return Err(INVALID);
        }
        let len = u32_at(bytes, cursor)? as usize;
        cursor += 4;
        let sid = Sid::parse(take(bytes, &mut cursor, len)?)?;
        let attributes = u32_at(bytes, cursor)?;
        cursor += 4;
        // Same attribute set accepted for token groups, without manufacturing
        // enabled or deny-only state for an omitted value.
        if attributes & !0xe000_007f != 0 || out.iter().any(|g| g.sid == sid) {
            return Err(INVALID);
        }
        out.push(SidAndAttributes { sid, attributes })?;
    }
    Ok(Some(out))
}

fn claims(bytes: &[u8], budget: &mut usize) -> KacsResult<Vec<ClaimAttribute>> {
    if bytes.len() > 65536 {
        return Err(INVALID);
    }
    let mut out = Vec::new();
    entries(bytes, |entry| {
        charge_claim(entry, budget)?;
        out.push(parse_claim_attribute_entry(entry)?)?;
        Ok(())
    })?;
    Ok(out)
}

fn charge_claim(entry: &[u8], budget: &mut usize) -> KacsResult<()> {
    let count = u32_at(entry, 12)? as usize;
    if count > MAX_ITEMS
        || entry.len() > 65536
        || entry.get(6..8) != Some(&[0, 0])
        || u32_at(entry, 8)? & !0x16 != 0
    {
        return Err(INVALID);
    }
    // Repeated offsets may otherwise expand a small untrusted entry into
    // gigabytes of decoded strings. Charge before any typed value allocation,
    // across subject namespaces AND descriptor resource attributes.
    let cost = entry.len().checked_mul(count.max(1)).ok_or(INVALID)?;
    *budget = budget.checked_sub(cost).ok_or(INVALID)?;
    Ok(())
}

fn absent(bytes: &[u8]) -> KacsResult<Vec<&str>> {
    let mut out = Vec::new();
    // The borrowed strings must refer to the owned ingress buffer, not to a
    // temporary entry or a userspace address.
    let mut cursor = 0;
    while cursor < bytes.len() {
        if out.len() >= MAX_ITEMS {
            return Err(INVALID);
        }
        let len = u32_at(bytes, cursor)? as usize;
        cursor += 4;
        if len == 0 || len > 255 {
            return Err(INVALID);
        }
        let name = core::str::from_utf8(take(bytes, &mut cursor, len)?).map_err(|_| INVALID)?;
        if name.contains('\0') {
            return Err(INVALID);
        }
        out.push(name)?;
    }
    Ok(out)
}

pub fn parse_subject_request(bytes: &[u8]) -> KacsResult<SubjectRequest<'_>> {
    if bytes.len() < HEADER_BYTES
        || bytes.len() > MAX_BYTES
        || u32_at(bytes, 0)? != VERSION
        || u32_at(bytes, 4)? as usize != bytes.len()
        || u32_at(bytes, 8)? & !NO_AUDIT != 0
        || u32_at(bytes, 12)? & !3 != 0
        || u32_at(bytes, 40)? & !7 != 0
        || u32_at(bytes, 44)? != 0
    {
        return Err(INVALID);
    }
    let mut sections = [&[][..]; 13];
    let mut cursor = HEADER_BYTES;
    for (i, section) in sections.iter_mut().enumerate() {
        let offset = u32_at(bytes, 48 + i * 8)? as usize;
        let len = u32_at(bytes, 52 + i * 8)? as usize;
        if len == 0 {
            if offset != 0 {
                return Err(INVALID);
            }
        } else {
            if offset != cursor {
                return Err(INVALID);
            }
            *section = take(bytes, &mut cursor, len)?;
        }
    }
    if cursor != bytes.len() {
        return Err(INVALID);
    }
    let sd = SecurityDescriptor::parse(sections[0])?;
    let known = u32_at(bytes, 12)?;
    let tree_bytes = sections[11];
    if tree_bytes.len() % 20 != 0 || tree_bytes.len() / 20 > MAX_ITEMS {
        return Err(INVALID);
    }
    let mut nodes = Vec::new();
    for entry in tree_bytes.chunks_exact(20) {
        if entry[2..4] != [0, 0] {
            return Err(INVALID);
        }
        nodes.push(ObjectTypeNode {
            level: u16::from_le_bytes([entry[0], entry[1]]),
            guid: entry[4..20].try_into().map_err(|_| INVALID)?,
        })?;
    }
    let tree = if nodes.is_empty() {
        None
    } else {
        Some(ObjectTypeList::new(&nodes)?)
    };
    let node = u32_at(bytes, 36)? as usize;
    if tree.as_ref().map_or(node != 0, |tree| node >= tree.len()) {
        return Err(INVALID);
    }
    let audit_context = if sections[12].is_empty() {
        None
    } else {
        if sections[12].len() > 4096 {
            return Err(INVALID);
        }
        crate::access_check_abi::parse_audit_context_map(sections[12])?;
        Some(sections[12])
    };
    let mut decode_budget = MAX_BYTES;
    if let Some(sacl) = sd.sacl() {
        for ace in sacl.entries() {
            if let crate::ace::AceKind::ResourceAttribute {
                application_data, ..
            } = ace?.kind()
            {
                charge_claim(application_data, &mut decode_budget)?;
            }
        }
    }
    let request = SubjectRequest {
        flags: u32_at(bytes, 8)?,
        desired: u32_at(bytes, 16)?,
        mapping: GenericMapping {
            read: u32_at(bytes, 20)?,
            write: u32_at(bytes, 24)?,
            execute: u32_at(bytes, 28)?,
            all: u32_at(bytes, 32)?,
        },
        node,
        sd,
        tree,
        audit_context,
        user: optional_sid(sections[1])?,
        groups: groups(sections[2], known & 1 != 0)?,
        device_groups: groups(sections[3], known & 2 != 0)?,
        claims: [
            claims(sections[4], &mut decode_budget)?,
            claims(sections[5], &mut decode_budget)?,
            claims(sections[6], &mut decode_budget)?,
        ],
        absent: [
            absent(sections[7])?,
            absent(sections[8])?,
            absent(sections[9])?,
        ],
        coverage: u32_at(bytes, 40)?,
        self_sid: optional_sid(sections[10])?,
    };
    // Validate even unused/unknown-policy claims: no conflicting or duplicate
    // names may hide in a request just because this descriptor ignores them.
    let subject = request.subject();
    subject.user_claims.validate()?;
    subject.device_claims.validate()?;
    subject.local_claims.validate()?;
    Ok(request)
}
