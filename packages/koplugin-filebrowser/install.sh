#!/bin/sh
# KOReader needs _meta.lua/main.lua at the plugin root, but the release ships
# them under src/. Flatten src/ to the root and keep the binary under filebrowser/.
DEST=/mnt/us/koreader/plugins/filebrowser.koplugin
mkdir -p "$DEST/filebrowser"
cp -f ./filebrowser.koplugin/src/_meta.lua ./filebrowser.koplugin/src/main.lua "$DEST/"
cp -f ./filebrowser.koplugin/filebrowser/filebrowser "$DEST/filebrowser/filebrowser"
chmod +x "$DEST/filebrowser/filebrowser"
