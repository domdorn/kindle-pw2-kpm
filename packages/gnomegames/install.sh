#!/bin/sh
mkdir -p /mnt/us/extensions/gnomegames
cp -rf ./gnomegames/. /mnt/us/extensions/gnomegames/
chmod +x /mnt/us/extensions/gnomegames/bin/armel/*
chmod +x /mnt/us/extensions/gnomegames/bin/armhf/*
chmod +x /mnt/us/extensions/gnomegames/bin/*.sh

cp -f ./scriptlets/GnomeGames.sh /mnt/us/documents/GnomeGames.sh
chmod +x /mnt/us/documents/GnomeGames.sh
mkdir -p "/mnt/us/documents/GnomeGames.sh.sdr"
cp -rf "./scriptlets/GnomeGames.sh.sdr/." "/mnt/us/documents/GnomeGames.sh.sdr/"
