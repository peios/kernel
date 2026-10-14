/* SPDX-License-Identifier: GPL-2.0 */

/*
 * perf's bench table calls these functions through pointers. Built with
 * -fcf-protection, each needs an endbr64 landing pad, and the object needs
 * the IBT/SHSTK property note or the linked perf loses both; <cet.h>
 * provides _CET_ENDBR and the note (and neither without __CET__).
 */
#include <cet.h>
#define SYM_START(name, linkage, align...)		\
	linkage(name) ASM_NL align ASM_NL name: ASM_NL _CET_ENDBR

// memset_orig is being defined as SYM_L_LOCAL but we need it
#define SYM_FUNC_START_LOCAL(name)                      \
        SYM_START(name, SYM_L_GLOBAL, SYM_A_ALIGN)
#define memset MEMSET /* don't hide glibc's memset() */
#define altinstr_replacement text
#define globl p2align 4; .globl
#include "../../arch/x86/lib/memset_64.S"

/*
 * We need to provide note.GNU-stack section, saying that we want
 * NOT executable stack. Otherwise the final linking will assume that
 * the ELF stack should not be restricted at all and set it RWX.
 */
.section .note.GNU-stack,"",@progbits
