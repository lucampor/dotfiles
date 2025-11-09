#!/bin/bash
eww open projects &

# Apply wallpaper using wal
wal -f ~/.config/wal/colorschemes/dark/oceanic-next.json &

# Start picom
picom --config ~/.config/picom/picom.conf &
