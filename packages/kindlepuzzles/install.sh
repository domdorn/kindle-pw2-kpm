#!/bin/sh
cp -rf ./kindlepuzzles/puzzles /mnt/us/puzzles
chmod +x /mnt/us/puzzles/hf/* /mnt/us/puzzles/pw2/*

mkdir -p /mnt/us/extensions/puzzles
cp -rf ./kindlepuzzles/extensions/puzzles/. /mnt/us/extensions/puzzles/

cp -f ./kindlepuzzles/documents/puzzles.sh /mnt/us/documents/puzzles.sh
chmod +x /mnt/us/documents/puzzles.sh
