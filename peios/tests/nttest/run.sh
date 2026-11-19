#!/bin/bash
# PEI-1720: run the NT handle semantics checks as SYSTEM on each managed
# filesystem the test VM has, then a generic-mapping check through sd.
runtime=/lcl/radius-dev/current
export PATH=$runtime/bin:$PATH LD_LIBRARY_PATH=$runtime/lib
nttest=/mnt/dev/nttest/nttest
sddl='O:SYG:SYD:P(A;OICI;GA;;;SY)(A;OICI;GA;;;BA)'
echo "--- identity"
id 2>&1 | head -1

# A StrataFS stack over ext4, with four files only in the lower stratum.
s=/var/state/ntsfs
rm -rf "$s"
mkdir -p "$s/up" "$s/lo" "$s/m/nt"
sd set "$s/up" "$sddl" >/dev/null
sd set "$s/lo" "$sddl" >/dev/null
mkdir -p "$s/lo/nt" "$s/up/nt"
echo x >"$s/lo/nt/cu"
echo x >"$s/lo/nt/cu2"
echo x >"$s/lo/nt/cu3"
echo x >"$s/lo/nt/cu4"
$nttest --mount "$s/m" "$s/up+create:$s/lo" && echo "--- mounted $s/m"

for d in /srv/nt /tmp/nt /var/state/nt "$s/m/nt"; do
    mkdir -p "$d" || continue
    sd set "$d" "$sddl" >/dev/null
    echo "--- $d on $(stat -f -c %T "$d")"
    if [ "$d" = "$s/m/nt" ]; then
        NTTEST_UPPER="$s/up/nt" $nttest "$d"
    else
        $nttest "$d"
    fi
done
echo "--- generic mapping on set"
mkdir -p /srv/nt/gm
sd set /srv/nt/gm 'O:SYG:SYD:P(A;;GA;;;SY)(A;OICI;GA;;;BA)'
sd show /srv/nt/gm
echo "--- kernel messages"
$nttest --kmsg
