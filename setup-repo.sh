#!/bin/sh
KPM="/var/local/kmc/bin/kpm"
SU="/var/local/kmc/bin/su"
$SU -c "$KPM --fbink add-repo https://dominikdorn.com/kpm/manifest.v2.json"
sleep 4
$SU -c "$KPM --fbink list-repo"
sleep 4
$SU -c "$KPM --fbink update"
sleep 4
/usr/bin/xrefresh -d :0.0
