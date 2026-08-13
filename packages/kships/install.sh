#!/bin/sh
APP_ID="xyz.lotpl.kships"
TARGET_DIR="/var/local/mesquite/KShips"
DB="/var/local/appreg.db"

mkdir -p "$TARGET_DIR"
cp -rf ./kships/KShips/. "$TARGET_DIR/"

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

cp -f ./scriptlets/KShips.sh /mnt/us/documents/KShips.sh
chmod +x /mnt/us/documents/KShips.sh
mkdir -p "/mnt/us/documents/KShips.sh.sdr"
cp -rf "./scriptlets/KShips.sh.sdr/." "/mnt/us/documents/KShips.sh.sdr/"
