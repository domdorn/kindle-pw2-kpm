#!/bin/sh
mkdir -p /var/local/mesquite/kanki
cp -rf ./kanki/kanki/. /var/local/mesquite/kanki/

# Register app in appreg.db
sqlite3 /var/local/appreg/appreg.db "INSERT OR REPLACE INTO application (app_id, hidden) VALUES ('xyz.kurizu.kanki', 0);"
sqlite3 /var/local/appreg/appreg.db "INSERT OR REPLACE INTO property (app_id, name, value) VALUES ('xyz.kurizu.kanki', 'command', '/usr/bin/mesquite');"
sqlite3 /var/local/appreg/appreg.db "INSERT OR REPLACE INTO property (app_id, name, value) VALUES ('xyz.kurizu.kanki', 'name', 'KAnki');"
sqlite3 /var/local/appreg/appreg.db "INSERT OR REPLACE INTO property (app_id, name, value) VALUES ('xyz.kurizu.kanki', 'config', '/var/local/mesquite/kanki/config.xml');"

cp -f ./scriptlets/KAnki.sh /mnt/us/documents/KAnki.sh
chmod +x /mnt/us/documents/KAnki.sh
mkdir -p "/mnt/us/documents/KAnki.sh.sdr"
cp -rf "./scriptlets/KAnki.sh.sdr/." "/mnt/us/documents/KAnki.sh.sdr/"
