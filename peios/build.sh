#!/bin/bash
# Kbuild runs only inside the pinned image, against a private source copy.
set -euo pipefail
profile=$1
jobs=$2
cd /work/src
test "$(rustc --version | cut -d' ' -f2)" = "$PEIOS_RUST_VERSION"
test "$(bindgen --version | cut -d' ' -f2)" = "$PEIOS_BINDGEN_VERSION"
export KBUILD_BUILD_USER=pkm KBUILD_BUILD_HOST=pkm-build KBUILD_BUILD_VERSION=1
export KBUILD_BUILD_TIMESTAMP="@$SOURCE_DATE_EPOCH"
export KCONFIG_NOTIMESTAMP=1
mkdir -p /work/out

# Keep equal generated inputs untouched so Kbuild can reuse its object files.
write_changed() {
    if ! cmp -s "$1" "$2"; then cp "$1" "$2"; fi
}
if [[ $profile == production ]]; then
    cert=peios/keys/dev-modsig.pem
    python3 peios/generate-keys.py --pubkey-hex "$(cat peios/keys/dev-tcb.hex)" --out /tmp/keys.h
else
    cert=peios/keys/kunit-modsig.pem
    python3 peios/generate-keys.py --allow-empty --out /tmp/keys.h
fi
write_changed /tmp/keys.h security/pkm/kacs/builtin_signing_keys.h
write_changed "$cert" certs/peios-modsig.pem

make_args=(make -C /work/src O=/work/out LLVM="$PEIOS_LLVM" CC="clang$PEIOS_LLVM")
# Kbuild's own host programs, fixdep and objtool say, are compiled by
# clang unless told otherwise. pekit's build tells it the pinned GCC
# toolchain, whose glibc sysroot they need; the kernel is still clang's.
if [[ -n ${PEIOS_HOSTCC:-} ]]; then
    make_args+=(HOSTCC="$PEIOS_HOSTCC" HOSTCXX="${PEIOS_HOSTCXX:?PEIOS_HOSTCXX goes with PEIOS_HOSTCC}")
fi
cp peios/config/config.x86_64.base /work/out/.config
"${make_args[@]}" olddefconfig
if [[ $profile == kunit ]]; then
    LSMOD=/work/src/peios/config/lsmod.txt "${make_args[@]}" localmodconfig
fi
KCONFIG_CONFIG=/work/out/.config scripts/kconfig/merge_config.sh -m -O /work/out \
    /work/out/.config peios/config/pkm.fragment
if [[ $profile == kunit ]]; then
    KCONFIG_CONFIG=/work/out/.config scripts/kconfig/merge_config.sh -m -O /work/out \
        /work/out/.config peios/config/kunit.fragment
fi
scripts/config --file /work/out/.config --set-str MODULE_SIG_KEY certs/peios-modsig.pem
scripts/config --file /work/out/.config --set-str LOCALVERSION "$PEIOS_LOCALVERSION"
"${make_args[@]}" olddefconfig
if [[ $profile == kunit ]]; then "${make_args[@]}" mod2yesconfig; fi
bash peios/verify-config.sh /work/out/.config
basever=$(make -s kernelversion)
debug_root="/usr/src/debug/kernel-$basever"
"${make_args[@]}" -j"$jobs" \
    KCFLAGS="-gno-record-gcc-switches -fdebug-prefix-map=/work/src=$debug_root -fmacro-prefix-map=/work/src=$debug_root -fdebug-prefix-map=/work/out=$debug_root -fmacro-prefix-map=/work/out=$debug_root" \
    KRUSTFLAGS="--remap-path-prefix=/work/src=$debug_root --remap-path-prefix=/work/out=$debug_root"
bash peios/verify-config.sh /work/out/.config
