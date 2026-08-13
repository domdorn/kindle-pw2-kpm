#!/bin/sh
rm -f /mnt/us/documents/lark.sh
if [ ! "$1" = "upgrade" ]; then
    rm -rf /mnt/us/LARK
    rm -rf /mnt/us/extensions/lark
fi
