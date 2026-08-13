#!/bin/sh
mkdir -p /mnt/us/filemanagers
cp -rf ./kindlefilemanagers/filemanagers/. /mnt/us/filemanagers/
chmod +x /mnt/us/filemanagers/bin/filebrowser
chmod +x /mnt/us/filemanagers/bin/syncthing
chmod +x /mnt/us/filemanagers/*.sh

mkdir -p /mnt/us/extensions/filemanagers
cp -rf ./kindlefilemanagers/extensions/filemanagers/. /mnt/us/extensions/filemanagers/

cp -f ./kindlefilemanagers/documents/filemanagers.sh /mnt/us/documents/filemanagers.sh
chmod +x /mnt/us/documents/filemanagers.sh
