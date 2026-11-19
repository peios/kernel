/* SPDX-License-Identifier: GPL-2.0-only */
#ifndef _SECURITY_PKM_KACS_NT_PIN_H
#define _SECURITY_PKM_KACS_NT_PIN_H

#include <linux/fs.h>
#include <linux/types.h>

/*
 * Ancestor pinning (TRM "Ancestor pinning"): while an open made with
 * KACS_OPEN_PIN_ANCESTORS lasts, the directories above the file, up to the
 * root of the mount it was opened through, cannot be renamed or removed.
 */

/* Pin @file's ancestors if @how_flags asks; the privilege is checked. */
int pkm_kacs_pin_ancestors_for_open(struct file *file, u32 how_flags);
/* Release an open's pins, as it closes. */
void pkm_kacs_pin_release(struct file *file);

bool pkm_kacs_pin_file_pinned(struct file *file);
/* Whether a directory is pinned by an open beneath it. */
bool pkm_kacs_pin_dentry_pinned(struct dentry *dentry);

#endif /* _SECURITY_PKM_KACS_NT_PIN_H */
