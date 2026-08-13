#!/bin/sh
rm -f /mnt/us/documents/filemanagers.sh
if [ ! "$1" = "upgrade" ]; then
    rm -rf /mnt/us/filemanagers
    rm -rf /mnt/us/extensions/filemanagers
fi
