#!/bin/sh
mkdir -p /mnt/us/extensions/gnomegames
cp -rf ./gnomegames/. /mnt/us/extensions/gnomegames/
chmod +x /mnt/us/extensions/gnomegames/bin/armel/*
chmod +x /mnt/us/extensions/gnomegames/bin/armhf/*
chmod +x /mnt/us/extensions/gnomegames/bin/*.sh

cp -f ./scriptlets/GnomeChess.sh /mnt/us/documents/GnomeChess.sh
chmod +x /mnt/us/documents/GnomeChess.sh

cp -f ./scriptlets/GnoMines.sh /mnt/us/documents/GnoMines.sh
chmod +x /mnt/us/documents/GnoMines.sh

rm -f /mnt/us/documents/GnomeGames.sh
rm -rf /mnt/us/documents/GnomeGames.sh.sdr
