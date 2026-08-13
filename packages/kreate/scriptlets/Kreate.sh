#!/bin/sh
APP_ID="xyz.foskya.kreate"
nohup lipc-set-prop com.lab126.appmgrd start app://$APP_ID >/dev/null 2>&1 &
