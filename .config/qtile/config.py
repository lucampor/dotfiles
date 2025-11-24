from libqtile import bar, layout, widget, hook, qtile
from libqtile.config import Click, Drag, Group, Key, Match, hook, Screen, KeyChord
from libqtile.lazy import lazy
from libqtile.utils import guess_terminal
from libqtile.dgroups import simple_key_binder
from time import sleep

mod = "mod4"
terminal = "alacritty"

# █▄▀ █▀▀ █▄█ █▄▄ █ █▄░█ █▀▄ █▀
# █░█ ██▄ ░█░ █▄█ █ █░▀█ █▄▀ ▄█

bg_col = "#e8d7ab"#333333"
bg_col2 = "#c14e4e"#CCCCCC"
bg_color3 = "#462d0e"#474747"




keys = [

#  D E F A U L T

    Key([mod], "h", lazy.layout.left(), desc="Move focus to left"),
    Key([mod], "l", lazy.layout.right(), desc="Move focus to right"),
    Key([mod], "j", lazy.layout.down(), desc="Move focus down"),
    Key([mod], "k", lazy.layout.up(), desc="Move focus up"),
    Key([mod], "space", lazy.layout.next(), desc="Move window focus to other window"),
    Key([mod, "control"], "h", lazy.layout.shuffle_left(), desc="Move window to the left"),
    Key([mod, "control"], "l", lazy.layout.shuffle_right(), desc="Move window to the right"),
    Key([mod, "control"], "j", lazy.layout.shuffle_down(), desc="Move window down"),
    Key([mod, "control"], "k", lazy.layout.shuffle_up(), desc="Move window up"),
    Key([mod, "shift"], "h", lazy.layout.grow_left(), desc="Grow window to the left"),
    Key([mod, "shift"], "l", lazy.layout.grow_right(), desc="Grow window to the right"),
    Key([mod, "shift"], "j", lazy.layout.grow_down(), desc="Grow window down"),
    Key([mod, "shift"], "k", lazy.layout.grow_up(), desc="Grow window up"),
    Key([mod, "shift"], "n", lazy.layout.normalize(), desc="Reset all window sizes"),
    Key([mod], "f", lazy.window.toggle_fullscreen()),
    Key(
        [mod, "shift"],
        "Return",
        lazy.layout.toggle_split(),
        desc="Toggle between split and unsplit sides of stack",
    ),
    Key([mod], "Return", lazy.spawn("kitty"), desc="Launch terminal"),
    Key([mod, "control"], "Return", lazy.spawn("kitty tmux"), desc="Launch terminal"),
    Key([mod], "Tab", lazy.next_layout(), desc="Toggle between layouts"),
    Key([mod], "q", lazy.window.kill(), desc="Kill focused window"),
    Key([mod, "control"], "r", lazy.reload_config(), desc="Reload the config"),
    Key([mod, "control"], "q", lazy.shutdown(), desc="Shutdown Qtile"),
    Key([mod], "d", lazy.spawn("sh -c ~/.config/rofi/scripts/launcher"), desc="Spawn a command using a prompt widget"),
    Key([mod], "x", lazy.spawn("sh -c ~/.config/rofi/scripts/power"), desc='powermenu'),
    #XXXKey([mod], "t", lazy.spawn("sh -c ~/.config/rofi/scripts/theme_switcher"), desc='theme_switcher'),


# C U S T O M

    Key([], "XF86AudioRaiseVolume", lazy.spawn("pactl set-sink-volume 0 +5%"), desc='Volume Up'),
    Key([], "XF86AudioLowerVolume", lazy.spawn("pactl set-sink-volume 0 -5%"), desc='volume down'),
    Key([], "XF86AudioMute", lazy.spawn("pulsemixer --toggle-mute"), desc='Volume Mute'),
    Key([], "XF86AudioPlay", lazy.spawn("playerctl play-pause"), desc='playerctl'),
    Key([], "XF86AudioPrev", lazy.spawn("playerctl previous"), desc='playerctl'),
    Key([], "XF86AudioNext", lazy.spawn("playerctl next"), desc='playerctl'),
    Key([], "XF86MonBrightnessUp", lazy.spawn("brightnessctl s 10%+"), desc='brightness UP'),
    Key([], "XF86MonBrightnessDown", lazy.spawn("brightnessctl s 10%-"), desc='brightness Down'),
    Key([mod],"e", lazy.spawn("emacsclient -c --alternate-editor="" --no-wait")),# -e \'(org-agenda nil \"n\")\'"), desc='best editor ever'),
    Key([mod, "shift"],"e", lazy.spawn("kitty nvim"), desc='second-to-best editor ever'),
	#Key([mod], "h", lazy.spawn("roficlip"), desc='clipboard'),
    Key([mod], "s", lazy.spawn("flameshot gui"), desc='Screenshot'),
    Key([mod], "w", lazy.spawn("waterfox")),
    Key([mod], "n", lazy.spawn("kitty ranger")),
    Key([mod, "shift"], "n", lazy.spawn("thunar")),
    Key(["mod1"], "Tab", lazy.group.next_window(), desc="Cycle to next window"),
    Key(["mod1", "shift"], "Tab", lazy.group.prev_window(), desc="Cycle to previous window"),

]



# █▀▀ █▀█ █▀█ █░█ █▀█ █▀
# █▄█ █▀▄ █▄█ █▄█ █▀▀ ▄█



labels = "🀢🀣🀤🀥🀦🀧🀩🀨🀪🀅"
groups = [Group(f"{(i+1) % 10}", label=labels[i]) for i in range(10)]

for i in groups:
    keys.extend(
            [
                Key(
                    [mod],
                    i.name,
                    lazy.group[i.name].toscreen(),
                    desc="Switch to group {}".format(i.name),
                    ),
                Key(
                    [mod, "shift"],
                    i.name,
                    lazy.window.togroup(i.name, switch_group=True),
                    desc="Switch to & move focused window to group {}".format(i.name),
                    ),
                ]
            )




# L A Y O U T S



lay_config = {
    "border_width": 5,
    "margin": 1,
    "border_focus": "123455",
    "border_normal": "3b4252",
    "font": "CaskaydiaCove Nerd Font",
    "grow_amount": 2,
}

layouts = [
    # layout.MonadWide(**lay_config),
    layout.Bsp(**lay_config, fair=False, border_on_single=False),
    layout.Columns(
        **lay_config,
        border_on_single=False,
        num_columns=2,
        split=False,
    ),
    # Plasma(lay_config, border_normal_fixed='#3b4252', border_focus_fixed='#3b4252', border_width_single=3),
    # layout.RatioTile(**lay_config),
    # layout.VerticalTile(**lay_config),
    # layout.Matrix(**lay_config, columns=3),
    # layout.Zoomy(**lay_config),
    # layout.Slice(**lay_config, width=1920, fallback=layout.TreeTab(), match=Match(wm_class="joplin"), side="right"),
    # layout.MonadTall(**lay_config),
    # layout.Tile(shift_windows=True, **lay_config),
    # layout.Stack(num_stacks=2, **lay_config),
    layout.Floating(**lay_config),
    layout.Max(**lay_config),
]



widget_defaults = dict(
    font="CaskaydiaCove Nerd Font",
    fontsize=12,
    padding=3,
)
extension_defaults = [ widget_defaults.copy()]
def search():
    qtile.cmd_spawn("sh -c ~/.config/rofi/scripts/launcher")

def power():
    qtile.cmd_spawn("sh -c ~/.config/rofi/scripts/power")


# █▄▄ ▄▀█ █▀█
# █▄█ █▀█ █▀▄



screens = [
    Screen(
        top=bar.Bar(
            [
                widget.Spacer(length=15, background=bg_col2),

                widget.Image(
                    filename='~/.config/qtile/Assets/launch_Icon.png',
                    margin=2,
                    background=bg_col2,
                    mouse_callbacks={"Button1": power},
                ),

                widget.Image(filename='~/.config/qtile/Assets/6.png'),

                widget.GroupBox(
                    font="CaskaydiaCove Nerd Font",
                    margin_y=7,
                    fontsize=38,
                    borderwidth=0,
                    highlight_method='block',
                    active='#462d0e',
                    block_highlight_text_color='#0e10c8',
                    highlight_color="#4B420E",#'#111',
                    inactive='#d4a66d',
                    foreground="#462d0e",
                    background=bg_col,
                    this_current_screen_border=bg_col,
                    center_aligned=True,
                    this_screen_border=bg_col,
                    other_current_screen_border=bg_col,
                    other_screen_border=bg_col,
                    urgent_border=bg_col,
                    rounded=True,
                    disable_drag=True,
                ),

                widget.Spacer(length=8, background=bg_col),

                widget.Image(filename='~/.config/qtile/Assets/1.png'),

                widget.CurrentLayout(
                    custom_icon_paths=["~/.config/qtile/Assets/layout"],
                    background=bg_col,
                    foreground=bg_color3,
                    scale=0.50,
                ),

                widget.Image(filename='~/.config/qtile/Assets/5.png'),

                widget.TextBox(
                    text=" ",
                    font="Font Awesome 6 Free Solid",
                    fontsize=13,
                    background=bg_col2,
                    foreground=bg_col,
                    mouse_callbacks={"Button1": search},
                ),

                widget.TextBox(
                    fmt='Search',
                    background=bg_col2,
                    font="JetBrainsMono Nerd Font Bold",
                    fontsize=13,
                    foreground=bg_col,
                    mouse_callbacks={"Button1": search},
                ),

                widget.Image(filename='~/.config/qtile/Assets/4.png'),

                widget.WindowName(
                    background=bg_col,
                    font="JetBrainsMono Nerd Font Bold",
                    fontsize=13,
                    empty_group_string="Desktop",
                    max_chars=130,
                    foreground=bg_color3,
                ),

                widget.Image(filename='~/.config/qtile/Assets/3.png'),

                widget.Systray(background=bg_col2, fontsize=2),

                widget.TextBox(text=' ', background=bg_col2),

                widget.Image(filename='~/.config/qtile/Assets/6.png', background=bg_col),

                widget.TextBox(
                    text="",
                    font="Font Awesome 6 Free Solid",
                    fontsize=13,
                    background=bg_col,
                    foreground=bg_color3,
                ),

                widget.Memory(
                    background=bg_col,
                    format='{MemUsed: .0f}{mm}',
                    foreground=bg_color3,
                    font="JetBrainsMono Nerd Font Bold",
                    fontsize=13,
                    update_interval=5,
                ),

                widget.Image(filename='~/.config/qtile/Assets/2.png'),

                widget.Spacer(length=8, background=bg_col),

                widget.TextBox(
                    text=" ",
                    font="Font Awesome 6 Free Solid",
                    fontsize=13,
                    background=bg_col,
                    foreground=bg_color3,
                ),

                widget.Battery(
                    font="JetBrainsMono Nerd Font Bold",
                    fontsize=13,
                    background=bg_col,
                    foreground=bg_color3,
                    format='{percent:2.0%}',
                ),

                widget.Image(filename='~/.config/qtile/Assets/2.png'),

                widget.Spacer(length=8, background=bg_col),

                widget.TextBox(
                    text=" ",
                    font="Font Awesome 6 Free Solid",
                    fontsize=13,
                    background=bg_col,
                    foreground=bg_color3,
                ),

				widget.Volume(
					font="JetBrainsMono Nerd Font Bold",
					fontsize=13,
					background=bg_col,
					foreground=bg_color3,
					mute_command="pamixer --toggle-mute",
					volume_up_command="pamixer -i 5",
					volume_down_command="pamixer -d 5",
					get_volume_command="pamixer --get-volume-human",
					update_interval=0.2,
					unmute_format="{volume}%",
					mute_format="M",
				),


                widget.Image(filename='~/.config/qtile/Assets/5.png', background=bg_col),

                widget.TextBox(
                    text=" ",
                    font="Font Awesome 6 Free Solid",
                    fontsize=13,
                    background=bg_col2,
                    foreground=bg_col,
                ),

                widget.Clock(
                    format='%I:%M %p',
                    background=bg_col2,
                    foreground=bg_col,
                    font="JetBrainsMono Nerd Font Bold",
                    fontsize=13,
                ),

                widget.Spacer(length=18, background=bg_col2),
            ],
            30,
            border_color=bg_col,
            border_width=[0, 0, 0, 0],
            margin=[15, 60, 6, 60],
        ),
    ),
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
	border_focus='#1F1D2E',
	border_normal='#1F1D2E',
	border_width=0,
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




import os
import subprocess
# stuff
@hook.subscribe.startup_once
def autostart():
    subprocess.call([os.path.expanduser('.config/qtile/autostart_once.sh')])

auto_fullscreen = True
focus_on_window_activation = "smart"
reconfigure_screens = True

# If things like steam games want to auto-minimize themselves when losing
# focus, should we respect this or not?
auto_minimize = True

# When using the Wayland backend, this can be used to configure input devices.
wl_input_rules = None

# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "LG3D"



# E O F
