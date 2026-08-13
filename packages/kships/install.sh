#!/bin/sh
mkdir -p /mnt/us/documents/KShips
cp -rf ./kships/KShips/. /mnt/us/documents/KShips/

cp -f ./kships/KShips.sh /mnt/us/documents/KShips.sh
chmod +x /mnt/us/documents/KShips.sh
mkdir -p "/mnt/us/documents/KShips.sh.sdr"
cp -rf "./scriptlets/KShips.sh.sdr/." "/mnt/us/documents/KShips.sh.sdr/"
