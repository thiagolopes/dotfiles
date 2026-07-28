#! /usr/bin/sh

set -e

layout=$(setxkbmap -query | grep layout | awk '{print $2}')
variant=$(setxkbmap -query | grep variant | awk '{print $2}')

echo "Keyboard ${layout}/${variant} init..."
setxkbmap -layout "$layout" -variant "$variant"
setxkbmap -option ctrl:nocaps

echo "Keyboard set rate...."
xset r rate 300 50

echo "Configure g610....."
g610-led -a ff
