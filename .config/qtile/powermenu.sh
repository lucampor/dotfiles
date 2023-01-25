#!/bin/env bash

# Options for powermenu
lock="    Lock"
logout="    Logout"
shutdown="    Shutdown"
reboot="    Reboot"
sleep="   Sleep"

# Get answer from user via rofi
selected_option=$(echo "$sleep
$logout
$reboot
$shutdown" | rofi -dmenu\
                  -i\
                  -p "Power"\
                  -font "Cascadia Code 12"\
                  -width "15"\
                  -lines 5\
                  -line-margin 3\
                  -line-padding 10\
                  -scrollbar-width "0" )

# Do something based on selected option
# if [ "$selected_option" == "$lock" ]
# then
#     /home/$USER/.config/scripts/i3lock-fancy/i3lock-fancy.sh
if [ "$selected_option" == "$logout" ]
then
    loginctl terminate-user luis
elif [ "$selected_option" == "$shutdown" ]
then
    systemctl poweroff
elif [ "$selected_option" == "$reboot" ]
then
    systemctl reboot
elif [ "$selected_option" == "$sleep" ]
then
    amixer set Master mute
    systemctl suspend
else
    echo "No match"
fi

