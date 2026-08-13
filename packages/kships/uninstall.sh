#!/bin/sh
rm -f /mnt/us/documents/KShips.sh
rm -rf /mnt/us/documents/KShips.sh.sdr
if [ ! "$1" = "upgrade" ]; then
    rm -rf /mnt/us/documents/KShips
    rm -rf /var/local/mesquite/KShips
fi
