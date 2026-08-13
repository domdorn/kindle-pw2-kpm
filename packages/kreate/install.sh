#!/bin/sh
APP_ID="xyz.foskya.kreate"
TARGET_DIR="/var/local/mesquite/kreate"
DB="/var/local/appreg/appreg.db"

mkdir -p "$TARGET_DIR"
cp -rf ./Kreate-main/kreate/. "$TARGET_DIR/"

sqlite3 "$DB" "INSERT OR REPLACE INTO application (app_id, hidden) VALUES ('$APP_ID', 0);"
sqlite3 "$DB" "INSERT OR REPLACE INTO property (app_id, name, value) VALUES ('$APP_ID', 'command', '/usr/bin/mesquite');"
sqlite3 "$DB" "INSERT OR REPLACE INTO property (app_id, name, value) VALUES ('$APP_ID', 'name', 'Kreate');"
sqlite3 "$DB" "INSERT OR REPLACE INTO property (app_id, name, value) VALUES ('$APP_ID', 'config', '$TARGET_DIR/config.xml');"

cp -f ./scriptlets/Kreate.sh /mnt/us/documents/Kreate.sh
chmod +x /mnt/us/documents/Kreate.sh
mkdir -p "/mnt/us/documents/Kreate.sh.sdr"
cp -rf "./scriptlets/Kreate.sh.sdr/." "/mnt/us/documents/Kreate.sh.sdr/"
