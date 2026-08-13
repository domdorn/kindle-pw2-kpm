#!/bin/sh
rm -f /mnt/us/documents/Gambatte.sh
rm -rf /mnt/us/documents/Gambatte.sh.sdr
if [ ! "$1" = "upgrade" ]; then
    rm -rf /mnt/us/extensions/gambatte-k2
fi
