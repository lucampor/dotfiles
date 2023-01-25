#!/usr/bin/env sh
# Qtile doesn't detect Alt Gr + 2 (= @)
setxkbmap -layout es
# But I want my custom keybindings
xmodmap /home/luis/.Xmodmap

picom --config /home/luis/.config/picom/picom.conf & disown

#conky -c /home/luis/.config/conky/conky-qtile.rc
#conky -c /home/luis/.config/conky/agenda.rc

dunst -conf /home/luis/.config/dunst/dunstrc & disown

