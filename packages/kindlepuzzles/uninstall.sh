#!/bin/sh
rm -f /mnt/us/documents/puzzles.sh
if [ ! "$1" = "upgrade" ]; then
    rm -rf /mnt/us/puzzles
    rm -rf /mnt/us/extensions/puzzles
fi
