#!/bin/sh
mkdir -p /var/local/mesquite/kanki
cp -rf ./kanki/kanki/. /var/local/mesquite/kanki/

APP_ID="xyz.kurizu.kanki"
DB="/var/local/appreg.db"
sqlite3 "$DB" "INSERT OR IGNORE INTO interfaces(interface) VALUES('application');"
sqlite3 "$DB" "INSERT OR IGNORE INTO handlerIds(handlerId) VALUES('$APP_ID');"
sqlite3 "$DB" "INSERT OR REPLACE INTO properties(handlerId,name,value) VALUES('$APP_ID','lipcId','$APP_ID');"
sqlite3 "$DB" "INSERT OR REPLACE INTO properties(handlerId,name,value) VALUES('$APP_ID','command','/usr/bin/mesquite -l $APP_ID -c file:///var/local/mesquite/kanki/ -j');"

cp -f ./scriptlets/KAnki.sh /mnt/us/documents/KAnki.sh
chmod +x /mnt/us/documents/KAnki.sh
mkdir -p "/mnt/us/documents/KAnki.sh.sdr"
cp -rf "./scriptlets/KAnki.sh.sdr/." "/mnt/us/documents/KAnki.sh.sdr/"
