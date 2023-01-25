# Copyright (c) 2010 Aldo Cortesi
# Copyright (c) 2010, 2014 dequis
# Copyright (c) 2012 Randall Ma
# Copyright (c) 2012-2014 Tycho Andersen
# Copyright (c) 2012 Craig Barnes
# Copyright (c) 2013 horsik
# Copyright (c) 2013 Tao Sauvage
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from qtile_extras.popup.toolkit import *
from libqtile import bar, layout, widget, hook, qtile
from libqtile.config import Click, Drag, DropDown, Group, Key, Match, ScratchPad, Screen
from libqtile.lazy import lazy
from libqtile.utils import guess_terminal
import os
import random
from subprocess import call

def show_power_menu(qtile):
    general_conf = {
        "font": "FiraCode Nerd Font",
        "fontsize": 16
    }
    layout = PopupGridLayout(
        qtile,
        rows=2, cols=2,
        width=1000,
        height=800,
        controls=PopupText(text=os.popen("cat ~/agenda").read()),
        background="00000060",
        initial_focus=None,
    )

    layout.show(centered=True)

def is_dark(color: str) -> bool:
    denom = 255
    color = int(color[1:],16)
    r = (color >> 16) & 0xff
    g = (color >> 8) & 0xff
    b = (color >> 0) & 0xff
    value = 0.212 * r + 0.701 * g + 0.087 * b
    return (value / denom) < 0.25

mod = "mod4"
terminal = "alacritty"
home = os.path.expanduser("~")

keys = [
    # A list of available commands that can be bound to keys can be found
    # at https://docs.qtile.org/en/latest/manual/config/lazy.html
    # Switch between windows
    Key([mod], "h", lazy.layout.left(), desc="Move focus to left"),
    Key([mod], "l", lazy.layout.right(), desc="Move focus to right"),
    Key([mod], "j", lazy.layout.down(), desc="Move focus down"),
    Key([mod], "k", lazy.layout.up(), desc="Move focus up"),
    Key([mod], "space", lazy.layout.next(), desc="Move window focus to other window"),
    # Move windows between left/right columns or move up/down in current stack.
    # Moving out of range in Columns layout will create new column.
    Key([mod, "shift"], "h", lazy.layout.shuffle_left(), desc="Move window to the left"),
    Key([mod, "shift"], "l", lazy.layout.shuffle_right(), desc="Move window to the right"),
    Key([mod, "shift"], "j", lazy.layout.shuffle_down(), desc="Move window down"),
    Key([mod, "shift"], "k", lazy.layout.shuffle_up(), desc="Move window up"),
    # Grow windows. If current window is on the edge of screen and direction
    # will be to screen edge - window would shrink.
    Key([mod, "control"], "h", lazy.layout.grow_left(), desc="Grow window to the left"),
    Key([mod, "control"], "l", lazy.layout.grow_right(), desc="Grow window to the right"),
    Key([mod, "control"], "j", lazy.layout.grow_down(), desc="Grow window down"),
    Key([mod, "control"], "k", lazy.layout.grow_up(), desc="Grow window up"),
    Key([mod], "m", lazy.layout.normalize(), desc="Reset all window sizes"),
    # Toggle between split and unsplit sides of stack.
    # Split = all windows displayed
    # Unsplit = 1 window displayed, like Max layout, but still with
    # multiple stack panes
    Key(
        [mod, "shift"],
        "Return",
        lazy.layout.toggle_split(),
        desc="Toggle between split and unsplit sides of stack",
    ),
    Key([mod], "Return", lazy.spawn(terminal), desc="Launch terminal"),
    # Toggle between different layouts as defined below
    Key([mod], "Tab", lazy.next_layout(), desc="Toggle between layouts"),
    Key([mod], "q", lazy.window.kill(), desc="Kill focused window"),
    Key([mod, "control"], "r", lazy.reload_config(), desc="Reload the config"),
    Key([mod, "control"], "q", lazy.shutdown(), desc="Shutdown Qtile"),
    Key([mod], "d", lazy.spawn("rofi -show drun"), desc="Start application"),
    Key([mod], "e", lazy.spawn("emacs"), desc="Yeah baby that's what I've been waiting for, that's what is all about"),
    Key([mod], "w", lazy.spawn("librewolf"), desc="Browser"),
    Key([mod], "x", lazy.spawn(home + "/.config/qtile/powermenu.sh"), desc="File Manager"),#function(show_power_menu)),

    Key([], 'XF86AudioRaiseVolume', lazy.spawn('amixer sset Master 5%+ unmute')),
    Key([], 'XF86AudioLowerVolume', lazy.spawn('amixer sset Master 5%- unmute')),
    Key([], 'XF86AudioMute', lazy.spawn('amixer -q set Master toggle')),

    # Brightness
    Key([], 'XF86MonBrightnessUp', lazy.spawn('brightnessctl s +5%')),
    Key([], 'XF86MonBrightnessDown', lazy.spawn('brightnessctl s 5%-')),
    # My screenshot key doesn't work (damn you Asus' Drivers)
    Key([mod, "shift"], 'f', lazy.spawn('flameshot gui')),

]

wallpapers = []
wallpaper_path = home + "/Pictures/Wallpapers"

for img in os.listdir(wallpaper_path):
    full_path = os.path.join(wallpaper_path, img)
    if os.path.isfile(full_path):
        wallpapers.append(img)

choice = random.choice(wallpapers)
wallpaper = os.path.join(wallpaper_path, choice)
os.system('python3 -m pywal -q -i ' + wallpaper  + ' --saturate 0.5') #+ ' --backend wal')#haishoku')
colors = []

with open(home + '/.cache/wal/colors', 'r') as file:
    for i in range(8):
        colors.append(file.readline().strip())
colors.append('#ffffff')

icons = ""
groups = []
for i in range(len(icons)):
    if i != 2:
        groups.append(Group(str(i+1), label=icons[i]))
    else:
        groups.append(Group(str(i+1), label=icons[i]))#, spawn="emacs"))
for i in groups:
    keys.extend(
        [
            # mod1 + letter of group = switch to group
            Key(
                [mod],
                i.name,
                lazy.group[i.name].toscreen(),
                desc="Switch to group {}".format(i.name),
            ),
            # mod1 + shift + letter of group = switch to & move focused window to group
            Key(
                [mod, "shift"],
                i.name,
                lazy.window.togroup(i.name, switch_group=False),
                desc="Switch to & move focused window to group {}".format(i.name),
            ),
            # Or, use below if you prefer not to switch to that group.
            # # mod1 + shift + letter of group = move focused window to group
            # Key([mod, "shift"], i.name, lazy.window.togroup(i.name),
            #     desc="move focused window to group {}".format(i.name)),
        ]
    )
groups.append(ScratchPad("scratchpad", [DropDown(name, f"{terminal} -e {name}",x=0.05, y=0.05, width=0.9, height=0.9, opacity=0.9, on_focus_lost_hide=False)
                                        for name in ["calcurse", "ranger", "htop", "taskwarrior-tui"]]
                                        + [DropDown("term",terminal, x=0.05, y=0.2, width=0.9, height=0.6, opacity=0.9, on_focus_lost_hide=True)],
                                        ))
keys.extend([
    Key([mod, "control"], "Return", lazy.group['scratchpad'].dropdown_toggle('term')),
    Key([mod], "c", lazy.group['scratchpad'].dropdown_toggle('calcurse')),
    Key([mod], "n", lazy.group['scratchpad'].dropdown_toggle('ranger')),
    Key([mod], "t", lazy.group['scratchpad'].dropdown_toggle('taskwarrior-tui')),
    ])

layouts = [
    layout.Columns(border_focus_stack=["#d75f5f", "#8f3d3d"], border_width=4),
    layout.Max(),
    # Try more layouts by unleashing below layouts.
    #layout.Stack(num_stacks=2),
    #layout.Bsp(),
    #layout.Matrix(),
    #layout.MonadTall(),
    #layout.MonadWide(),
    #layout.RatioTile(),
    #layout.Tile(),
    #layout.TreeTab(),
    #layout.VerticalTile(),
    #layout.Zoomy(),
]

def font_color(color):
    return colors[8] if is_dark(color) else colors[0]
widget_defaults = dict(
    font="JetBrainsMonoNL Nerd Font",
    fontsize=20,
    padding=6,
)

extension_defaults = widget_defaults.copy()
screens = [
    Screen(top=bar.Bar(
            [
                widget.GroupBox(
                    active=colors[8],
                    inactive=colors[0],
                    rounded=False,
                    highlight_color=colors[2],
                    highlight_method="line",
                    borderwidth=0
                ),
                widget.Spacer(length=bar.STRETCH),
                widget.WindowName(
                    markup=True,
                    fontsize=15,
                    foreground=colors[0],
                    max_chars=60
                ),
                # widget.TextBox(
                #     fmt="",
                #     padding=1.5,
                #     foreground=colors[6],
                #     background=colors[4]
                # ),
                # widget.CurrentLayout(
                #     fmt=" {}",
                #     background=colors[6],
                #     foreground=font_color(colors[6])
                # ),
                # widget.TextBox(
                #     fmt="",
                #     padding=1.5,
                #     foreground=colors[1],
                #     background=colors[4]
                # ),
                widget.Volume(
                    background=colors[1],
                    foreground=font_color(colors[1]),
                    fmt='Vol: {}',
                ),
                # widget.TextBox(
                #     fmt="",
                #     padding=1.5,
                #     foreground=colors[6],
                #     background=colors[1]
                # ),
                widget.CPUGraph(
                    background=colors[6],
                    border_color=colors[6],
                    fill_color=colors[4],
                    graph_color=colors[4],
                    mouse_callbacks =  {"Button1": lazy.group['scratchpad'].dropdown_toggle('htop')},
                ),
                # widget.TextBox(
                #     fmt="",
                #     padding=1.5,
                #     foreground=colors[1],
                #     background=colors[6]
                # ),
                widget.ThermalZone(
                    format=" {temp}°C",
                    fgcolor_normal=font_color(colors[1]),
                    high=60, crit=80,
                    background=colors[1],
                    zone="/sys/class/thermal/thermal_zone0/temp"
                ),
                # widget.TextBox(
                #     fmt="",
                #     padding=1.5,
                #     foreground=colors[6],
                #     background=colors[1]
                # ),
                widget.Memory(
                    format="溜{MemUsed: .2f}{mm}",
                    measure_mem="G",
                    background=colors[6],
                    foreground=font_color(colors[6]),
                    interval=1.0
                ),
                # widget.TextBox(
                #     fmt="",
                #     padding=1.5,
                #     foreground=colors[1],
                #     background=colors[6]
                # ),
                # widget.Net(
                #     interface="wlan0",
                #     format=" {interface}: {down} ↓↑ {up}",
                #     background=colors[1],
                #     foreground="#191724",
                #     update_interval=1.0
                # ),
                widget.Battery(
                    update_interval=5,
                    charge_char="",
                    discharge_char="",
                    full_char="",
                    unknown_char="",
                    empty_char="",
                    notify_below=0.2,
                    foreground=font_color(colors[1]),
                    low_percentage=0.25,
                    background=colors[1],
                ),
                # widget.TextBox(
                #     fmt="",
                #     padding=1.5,
                #     foreground=colors[6],
                #     background=colors[1]
                # ),
                widget.Clock(
                    background=colors[6],
                    foreground=font_color(colors[6]),
                    format=" %H:%M - %d/%m/%Y",
                    update_interval=60.0,
                    mouse_callbacks =  {"Button1": lazy.group['scratchpad'].dropdown_toggle('calendar')},
                ),
                # widget.TextBox(
                #     fmt="",
                #     padding=1.5,
                #     foreground=colors[1],
                #     background=colors[6]
                # ),
                # widget.Pomodoro(
                #     prefix_inactive="[Pomodoro]",
                #     background=colors[1],
                #     color_inactive=font_color(colors[1]),
                #     prefix_paused="[Paused]",
                # ),
                widget.Systray(
                    background=colors[6],
                ),
            ],
            28,
            background=colors[4],
        ),
    ),
        # top=bar.Bar(
        #     [
        #         widget.GroupBox(),
        #         #widget.CurrentLayout(),
        #         widget.Prompt(),
        #         widget.Chord(
        #             chords_colors={
        #                 "launch": ("#610e5c", "#ffffff"),
        #             },
        #             name_transform=lambda name: name.upper(),
        #         ),
        #         widget.Spacer(length=bar.STRETCH),
        #         widget.Clock(format="%Y-%m-%d %a %I:%M %p"),
        #         widget.Spacer(length=bar.STRETCH),

        #         # NB Systray is incompatible with Wayland, consider using StatusNotifier instead
        #         # widget.StatusNotifier(),
        #         widget.Systray(),
        #         widget.Volume(),
        #         #widget.Backlight(),
        #         widget.Battery(update_interval=5,
        #                        low_percentage=0.2,),
        #         widget.Pomodoro(
        #             prefix_inactive="[Pomodoro]",
        #             color_inactive="ffffff",
        #             prefix_paused="[Paused]",
        #         ),
        #     ],
        #     size=34,
        #     # border_width=[2, 0, 2, 0],  # Draw top and bottom borders
        #     # border_color=["ff00ff", "000000", "ff00ff", "000000"]  # Borders are magenta
        # ),

]

# Drag floating layouts.
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(), start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(), start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front()),
]



dgroups_key_binder = None
dgroups_app_rules = []  # type: list
follow_mouse_focus = True
bring_front_click = False
cursor_warp = False
floating_layout = layout.Floating(
    float_rules=[
        # Run the utility of `xprop` to see the wm class and name of an X client.
        *layout.Floating.default_float_rules,
        Match(wm_class="confirmreset"),  # gitk
        Match(wm_class="makebranch"),  # gitk
        Match(wm_class="maketag"),  # gitk
        Match(wm_class="ssh-askpass"),  # ssh-askpass
        Match(title="branchdialog"),  # gitk
        Match(title="pinentry"),  # GPG key password entry
    ]
)
auto_fullscreen = True
focus_on_window_activation = "smart"
reconfigure_screens = True

# If things like steam games want to auto-minimize themselves when losing
# focus, should we respect this or not?
auto_minimize = True

# When using the Wayland backend, this can be used to configure input devices.
wl_input_rules = None

wmname = "LG3D"

@hook.subscribe.startup_once
def startup_once():
    home = os.path.expanduser('~/.config/qtile/startup_once.sh')
    call([home])

@hook.subscribe.resume
def resume():
    home = os.path.expanduser('~/.config/qtile/resume.sh')
    call([home])
