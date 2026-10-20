/* SPDX-License-Identifier: GPL-2.0-only */
#ifndef _SECURITY_PKM_KACS_OVERLAY_BACKING_H
#define _SECURITY_PKM_KACS_OVERLAY_BACKING_H

struct file;

/*
 * Only for an unpublished staged open owned by the copy-up caller. Returns a
 * pinned exact upper child, NULL for a non-OverlayFS leaf, or an error.
 */
struct file *pkm_kacs_copy_up_overlay_child_get(struct file *file);

#endif /* _SECURITY_PKM_KACS_OVERLAY_BACKING_H */
