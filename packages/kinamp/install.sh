#!/bin/sh
cp -rf ./kinamp/KinAMP /mnt/us/KinAMP
chmod +x /mnt/us/KinAMP/KinAMP* /mnt/us/KinAMP/*.sh

mkdir -p /mnt/us/extensions/kinamp
cp -rf ./kinamp/extensions/kinamp/. /mnt/us/extensions/kinamp/

cp -f ./kinamp/documents/kinamp.sh /mnt/us/documents/kinamp.sh
chmod +x /mnt/us/documents/kinamp.sh

if [ -d /mnt/us/koreader/plugins ]; then
    cp -rf ./kinamp/koreader/plugins/kinamp.koplugin /mnt/us/koreader/plugins/
fi
