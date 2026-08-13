#!/bin/sh
mkdir -p /mnt/us/extensions/kterm
cp -rf ./kterm/. /mnt/us/extensions/kterm/
chmod +x /mnt/us/extensions/kterm/bin/kterm

cp -f ./scriptlets/KTerm.sh /mnt/us/documents/KTerm.sh
chmod +x /mnt/us/documents/KTerm.sh
mkdir -p "/mnt/us/documents/KTerm.sh.sdr"
cp -rf "./scriptlets/KTerm.sh.sdr/." "/mnt/us/documents/KTerm.sh.sdr/"
