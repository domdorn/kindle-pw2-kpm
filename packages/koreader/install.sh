#!/bin/sh

echo "Copying koreader folder"
cp -rf ./koreader /mnt/us/
rm -rf ./koreader
echo "Copying KOReader scriptlet"
if [ -f /mnt/us/documents/KOReader.sh ]; then
    rm -rf /mnt/us/documents/KOReader.sh
    sleep 1
fi
cp -ar ./scriptlets/KOReader.sh /mnt/us/documents/KOReader.sh
if [ -d /mnt/us/extensions ]; then
    echo "Copying KOReader KUAL extension"
    cp -rf ./extensions/koreader /mnt/us/extensions/
    rm -rf ./extensions
fi