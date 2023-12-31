#!/usr/bin/env bash
set -e

xorg_conf="/etc/X11/xorg.conf.d/40-libinput.conf"
template='
Section "InputClass"
    Identifier "libinput pointer catchall"
    MatchIsPointer "on"
    MatchDevicePath "/dev/input/event*"
    Driver "libinput"
    Option "NaturalScrolling" "True"
    Option "Tapping" "on"
EndSection
'

if [ -f "$xorg_conf" ]; then
    if grep -q "Option \"NaturalScrolling\" \"True\"" "$xorg_conf"; then
        echo "The 'NaturalScrolling' option is already configured in the file."
    else
        echo 'Option "NaturalScrolling" "True" - not configured in the file'
    fi
else
    echo "$template" | sudo tee "$xorg_conf" > /dev/null
    echo "Created '$xorg_conf' file with the 'Natural Scrolling' configuration."
fi
