#!/bin/sh
rm -f /mnt/us/documents/KAnki.sh
rm -rf /mnt/us/documents/KAnki.sh.sdr
sqlite3 /var/local/appreg/appreg.db "DELETE FROM property WHERE app_id='xyz.kurizu.kanki';"
sqlite3 /var/local/appreg/appreg.db "DELETE FROM application WHERE app_id='xyz.kurizu.kanki';"
if [ ! "$1" = "upgrade" ]; then
    rm -rf /var/local/mesquite/kanki
fi
