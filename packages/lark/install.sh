#!/bin/sh
cp -rf ./lark/LARK /mnt/us/LARK
chmod +x /mnt/us/LARK/larkplayer* /mnt/us/LARK/*.sh

mkdir -p /mnt/us/extensions/lark
cp -rf ./lark/extensions/lark/. /mnt/us/extensions/lark/

cp -f ./lark/documents/lark.sh /mnt/us/documents/lark.sh
chmod +x /mnt/us/documents/lark.sh
