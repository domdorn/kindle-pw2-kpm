#!/bin/sh
rm -f /mnt/us/documents/KTerm.sh
if [ ! "$1" = "upgrade" ]; then
    rm -rf /mnt/us/extensions/kterm
fi
