#!/bin/sh
mkdir -p /mnt/us/extensions/gambatte-k2
cp -rf ./gambatte-k2/. /mnt/us/extensions/gambatte-k2/
chmod +x /mnt/us/extensions/gambatte-k2/gambatte-k2-armel
chmod +x /mnt/us/extensions/gambatte-k2/gambatte-k2-armhf

cp -f ./scriptlets/Gambatte.sh /mnt/us/documents/Gambatte.sh
chmod +x /mnt/us/documents/Gambatte.sh
mkdir -p "/mnt/us/documents/Gambatte.sh.sdr"
cp -rf "./scriptlets/Gambatte.sh.sdr/." "/mnt/us/documents/Gambatte.sh.sdr/"
