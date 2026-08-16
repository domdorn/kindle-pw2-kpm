#!/bin/sh
rm -f /mnt/us/documents/kwordle.sh
if [ ! "$1" = "upgrade" ]; then
    rm -rf /mnt/us/documents/kwordle
fi
