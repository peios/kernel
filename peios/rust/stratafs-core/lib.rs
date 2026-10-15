//! Cargo entry point for the same semantic source compiled by Kbuild.

#![cfg_attr(not(test), no_std)]

#[path = "../../../security/pkm/stratafs_core/mod.rs"]
mod stratafs_core;

pub use stratafs_core::*;
