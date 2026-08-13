#!/bin/sh
rm -f /mnt/us/documents/GnomeChess.sh
rm -f /mnt/us/documents/GnoMines.sh
rm -f /mnt/us/documents/GnomeGames.sh
rm -rf /mnt/us/documents/GnomeGames.sh.sdr
if [ ! "$1" = "upgrade" ]; then
    rm -rf /mnt/us/extensions/gnomegames
fi
