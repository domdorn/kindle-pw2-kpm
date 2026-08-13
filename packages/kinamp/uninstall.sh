#!/bin/sh
rm -f /mnt/us/documents/kinamp.sh
if [ ! "$1" = "upgrade" ]; then
    rm -rf /mnt/us/KinAMP
    rm -rf /mnt/us/extensions/kinamp
    rm -rf /mnt/us/koreader/plugins/kinamp.koplugin
fi
