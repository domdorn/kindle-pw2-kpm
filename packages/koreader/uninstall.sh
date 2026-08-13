#!/bin/sh

echo "Deleting scriptlet for koreader"
rm /mnt/us/documents/KOReader.sh
echo "Deleting KOReader KUAL extension"
rm -rf /mnt/us/extensions/koreader
if [ ! "$1" = "upgrade" ]; then
    echo "Deleting KOReader folder"
    rm -rf /mnt/us/koreader
fi