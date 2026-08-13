#!/bin/sh
rm -f /mnt/us/documents/KAnki.sh
rm -rf /mnt/us/documents/KAnki.sh.sdr
DB="/var/local/appreg.db"
APP_ID="xyz.kurizu.kanki"
sqlite3 "$DB" "DELETE FROM properties WHERE handlerId='$APP_ID';"
sqlite3 "$DB" "DELETE FROM handlerIds WHERE handlerId='$APP_ID';"
if [ ! "$1" = "upgrade" ]; then
    rm -rf /var/local/mesquite/kanki
fi
