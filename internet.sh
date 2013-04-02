#!/bin/sh

case "$1" in
    on)
        sudo ufw disable 
        ;;
    off)
        sudo ufw enable
        ;;
    *)
        echo "Sorry only 'on' or 'off' arguments"
        exit 1
        ;;
esac

