#!/bin/sh
APP_ID="xyz.foskya.kreate"
TARGET_DIR="/var/local/mesquite/kreate"
DB="/var/local/appreg.db"

mkdir -p "$TARGET_DIR"
cp -rf ./kreate/Kreate-main/kreate/. "$TARGET_DIR/"

sqlite3 "$DB" <<EOF
INSERT OR IGNORE INTO interfaces(interface) VALUES('application');
INSERT OR IGNORE INTO handlerIds(handlerId) VALUES('$APP_ID');
INSERT OR REPLACE INTO properties(handlerId,name,value)
  VALUES('$APP_ID','lipcId','$APP_ID');
INSERT OR REPLACE INTO properties(handlerId,name,value)
  VALUES('$APP_ID','command','/usr/bin/mesquite -l $APP_ID -c file://$TARGET_DIR/');
INSERT OR REPLACE INTO properties(handlerId,name,value)
  VALUES('$APP_ID','supportedOrientation','U');
EOF

cp -f ./scriptlets/Kreate.sh /mnt/us/documents/Kreate.sh
chmod +x /mnt/us/documents/Kreate.sh
mkdir -p "/mnt/us/documents/Kreate.sh.sdr"
cp -rf "./scriptlets/Kreate.sh.sdr/." "/mnt/us/documents/Kreate.sh.sdr/"
