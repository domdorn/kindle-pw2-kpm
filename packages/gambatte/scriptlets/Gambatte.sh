#!/bin/sh
ARCH=$([ -f /lib/ld-linux-armhf.so.3 ] && echo "armhf" || echo "armel")
/mnt/us/extensions/gambatte-k2/gambatte-k2-$ARCH
