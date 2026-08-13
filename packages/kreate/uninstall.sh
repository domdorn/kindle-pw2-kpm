#!/bin/sh
APP_ID="xyz.foskya.kreate"
DB="/var/local/appreg/appreg.db"

rm -f /mnt/us/documents/Kreate.sh
rm -rf /mnt/us/documents/Kreate.sh.sdr

sqlite3 "$DB" "DELETE FROM property WHERE app_id='$APP_ID';"
sqlite3 "$DB" "DELETE FROM application WHERE app_id='$APP_ID';"

if [ ! "$1" = "upgrade" ]; then
    rm -rf /var/local/mesquite/kreate
fi
