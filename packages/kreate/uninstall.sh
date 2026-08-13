#!/bin/sh
APP_ID="xyz.foskya.kreate"
DB="/var/local/appreg.db"

rm -f /mnt/us/documents/Kreate.sh
rm -rf /mnt/us/documents/Kreate.sh.sdr

sqlite3 "$DB" "DELETE FROM properties WHERE handlerId='$APP_ID';"
sqlite3 "$DB" "DELETE FROM handlerIds WHERE handlerId='$APP_ID';"

if [ ! "$1" = "upgrade" ]; then
    rm -rf /var/local/mesquite/kreate
fi
