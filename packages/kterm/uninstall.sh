#!/bin/sh
rm -f /mnt/us/documents/KTerm.sh
rm -rf /mnt/us/documents/KTerm.sh.sdr
if [ ! "$1" = "upgrade" ]; then
    rm -rf /mnt/us/extensions/kterm
fi
