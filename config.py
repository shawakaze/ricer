# mod of the original

import re
import socket
import os
import sys
import subprocess


from typing import List  # noqa: F401

from libqtile import bar, layout, hook
from libqtile.config import Click, Drag, Group, Key, Match, Screen
from libqtile.lazy import lazy
from libqtile.utils import guess_terminal
from colors import *
from qtile_extras import widget 
from qtile_extras.widget.decorations import PowerLineDecoration
from qtile_extras.layout.decorations import ConditionalBorder, GradientBorder, GradientFrame, RoundedCorners

mod = "mod4"
#terminal = guess_terminal()
#terminal = "cool-retro-term"
terminal = "alacritty"
#terminal = "urxvt"

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
    Key([mod], "n", lazy.layout.normalize(), desc="Reset all window sizes"),
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
    Key([mod], "w", lazy.window.kill(), desc="Kill focused window"),
    Key([mod, "control"], "r", lazy.reload_config(), desc="Reload the config"),
    Key([mod, "control"], "q", lazy.shutdown(), desc="Shutdown Qtile"),
    Key([mod], "r", lazy.spawncmd(), desc="Spawn a command using a prompt widget"),
]

group_names = [
		("", {'layout': 'monadtall','matches':[Match(wm_class=["Alacritty","urxvt","URxvt","cool-retro-term"])]}),
		("", {'layout': 'monadtall','matches':[Match(wm_class=["vlc","smplayer","jellyfinmediaplayer","plexmediaplayer","netflix","Netflix"])]}), 
		("", {'layout': 'monadtall','matches':[Match(wm_class=["dolphin","thunar"])]}),
		("", {'layout':'monadtall','matches':[Match(wm_class=["Xiphos","xiphos"])]}),	
		("", {'layout': 'monadtall','matches':[Match(wm_class=["firefox","qutebrowser"])]}),
		("" , {'layout': 'monadtall','matches':[Match(wm_class=["chromium","Chromium"])]}),
		("", {'layout': 'max','matches':[Match(wm_class=["Kile","kile","Texmaker","texmaker","Texstudio","texstudio"])]}),
		("", {'layout': 'max','matches':[Match(wm_class=["libreoffice"])]}),
		("", {'layout': 'monadtall','matches':[Match(wm_class=["Evince","Zathura","zathura","Okular","okular"])]}),
		]

groups = [Group(name, **kwargs) for name, kwargs in group_names]

for i, (name, kwargs) in enumerate(group_names, 1):
    keys.append(Key([mod], str(i), lazy.group[name].toscreen()))        # Switch to another group
    keys.append(Key([mod, "shift"], str(i), lazy.window.togroup(name))) # Send current window to another group


monadtall_theme = dict(
        border_focus = volt, #RoundedCorners(colours=volt[1:4]),
        border_normal = bg_kala,
        border_width = 2,
        margin = 16
        )

layouts = [
    layout.Columns(**monadtall_theme), #border_focus_stack=["#d75f5f", "#8f3d3d"], border_width=4),
    layout.Max(),
    # Try more layouts by unleashing below layouts.
    #layout.Stack(num_stacks=2),
    layout.Bsp(),
    # layout.Matrix(),
    layout.MonadTall(**monadtall_theme),
    # layout.MonadWide(),
    # layout.RatioTile(),
    #layout.Tile(),
    # layout.TreeTab(),
    # layout.VerticalTile(),
    # layout.Zoomy(),
]

widget_defaults = dict(
    font = 'Mononoki Nerd Font',
    fontsize=18,
    padding=10,
    background = bg_kala,
    foreground = fg_kala
)
extension_defaults = widget_defaults.copy()

# additional colors
try:
	inverse = inv_volt
except:
	inverse = '#0c0e00'

powerlineL = {     
		"decorations": [  PowerLineDecoration(path="forward_slash")     ] 
		}
powerlineR = {     
		"decorations": [  PowerLineDecoration(path="back_slash")     ] 
		}
screens = [
    Screen(
        top=bar.Bar(
            [
		widget.Mpd2(background = volt, host = 'localhost', port = 6600, status_format = '{play_status} {title}', update_interval = 1, foreground =  bg_kala, **powerlineL),
 		widget.Prompt(background = bg_kala, foreground = volt, prompt = ""+' ' ), 
		widget.Spacer(background= bg_kala,**powerlineL),

                 widget.GroupBox(
		    #font = 'Font Awesome 6 Free',
		    fontsize = 23,
                    padding_x=7 ,
		    padding_y=3, 
                    spacing=7,
		    #margin_y = 1, 
                    borderwidth = 1, 
                    active = bg_kala,
		    #inactive = bg_kala, 
                    rounded = False, 
                    this_current_screen_border = fg_kala,
		    this_screen_border = volt,
		    other_screen_border = volt, 
                    highlight_method = "text", # Options: block, line, text. 
                    block_highlight_text_color = fg_kala,
		    disable_drag = True,
		    background = volt,
		    foreground = fg_kala,
		    **powerlineL,
                    ),              

                #widget.PulseVolume(foreground = volt,fmt=fa.icons['volume-up']+'{}',update_interval=0.2),
                #widget.OpenWeather(foreground = volt, app_key = '3bbca9935bdd06f3a56f955c4a70fba1',cityid = '909137', padding = 5),
                #widget.Spacer(length = 5),
		widget.Wlan(background = bg_kala, foreground = volt, interface='wlan0',format="  "+" {essid} {quality}/70"), #**powerlineL),
                widget.Net(
			   format = "  "+" {down:6.2f}{down_suffix:<2}/s "+"  "+" {up:6.2f}{up_suffix:<2}/s", 
			   update_interval = 1, 
			   foreground = volt, background = bg_kala, 
			   **powerlineL ),
		#widget.Net(format = ""+" {up:6.2f}{up_suffix:<2}/s", update_interval = 1, background = bg_kala, foreground = volt, **powerlineL),
                #widget.Memory(background = volt, foreground = bg_kala,format=fa.icons['database']+' {MemPercent}%', **powerlineL),
                #widget.CPU(update_interval=1, background = bg_kala, foreground = volt, format=fa.icons['microchip']+' {load_percent}%', **powerlineL),

                #widget.BatteryIcon(
		#	theme_path='/home/muzo/.config/qtile/icons/battery-icons',
		#	update_interval=2,
		#	background = bg_kala,
		#	foreground = volt, 
		#	**powerlineL),
                #widget.CurrentLayoutIcon(
                #    custom_icon_paths = [os.path.expanduser("~/.config/qtile/icons")],
                #    foreground = volt,
                #    background = bg_kala,
                #    scale = 0.7,
                #    padding = 5,
		#    **powerlineL
                #),
               widget.Systray(foreground = bg_kala, background = volt, **powerlineL),
               widget.Clock(format="%a %H:%M", foreground = volt,background = bg_kala),
                
            ],
            size=30, 
            opacity=0.65,
            border_width=[2, 2, 2, 2],  # Draw top and bottom borders
            border_color=volt, #["ff00ff", "000000", "ff00ff", "000000"]  # Borders are magenta
	    margin=[10,8,0,8]
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
dgroups_app_rules = []  # type: List

@hook.subscribe.startup_once
def start_once():
    home = os.path.expanduser('~')
    subprocess.call([home + '/.config/qtile/scripts/autostart.sh'])

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
    ],
	border_focus = volt,
	border_normal = bg_kala,
	border_width = 3
)

auto_fullscreen = True
focus_on_window_activation = "smart"
reconfigure_screens = True

# If things like steam games want to auto-minimize themselves when losing
# focus, should we respect this or not?
auto_minimize = True

# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "3L33T"
