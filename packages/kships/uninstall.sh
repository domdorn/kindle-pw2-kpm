#!/bin/sh
APP_ID="xyz.lotpl.kships"
DB="/var/local/appreg.db"

rm -f /mnt/us/documents/KShips.sh
rm -rf /mnt/us/documents/KShips.sh.sdr

sqlite3 "$DB" "DELETE FROM properties WHERE handlerId='$APP_ID';"
sqlite3 "$DB" "DELETE FROM handlerIds WHERE handlerId='$APP_ID';"

if [ ! "$1" = "upgrade" ]; then
    rm -rf /var/local/mesquite/KShips
fi
