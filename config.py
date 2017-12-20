#!/usr/bin/env python
# coding: utf-8

"""
I use this applications and utils:
    amixer, feh, firefox, gajim, gnome-terminal, nemo, rofi, scrot, vlc, xterm
"""

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

from glob import glob
from random import choice
from time import sleep
import os
import subprocess

from libqtile import layout, widget, bar, hook
from libqtile.widget import base
from libqtile.manager import Screen, Drag, Click
from libqtile.command import lazy
from libqtile.config import Key, Group


"""
def move_window_to_screen(screen):
    def cmd(qtile):
        w = qtile.currentWindow
        # XXX: strange behaviour - w.focus() doesn't work
        # if toScreen is called after togroup...
        qtile.toScreen(screen)
        if w is not None:
            w.togroup(qtile.screens[screen].group.name)
    return cmd
"""

################################################################################

KeyboardLayout = widget.KeyboardLayout(
    background='#FFFFFF',
    configured_keyboards=['us', 'ru'],
    font='Ubuntu',
    fontsize=14,
    foreground='#000000',
)
def next_keyboard():
    def cmd(qtile):
        return
        KeyboardLayout.next_keyboard()
    return cmd

################################################################################

font = 'Font Awesome'#'FreeMono Bold'
font2groups = 'Century Schoolbook L'
foreground = '#000000'
background = '#FFFFFF'
alert = "#FFFF00"
fontsize = 15

font_params = {
    'font': font,
    'fontsize': fontsize,
    'foreground': foreground,
	'background': background,
}

mod = 'mod1'
keys = [
    Key([mod], "h", lazy.hide_show_bar()),        
    Key([mod], "k", lazy.layout.down()),
    Key([mod], "j", lazy.layout.up()),
    Key([mod, "shift"], "k", lazy.layout.shuffle_down()),
    Key([mod, "shift"], "j", lazy.layout.shuffle_up()),
    Key([mod], "Tab", lazy.layout.next()),
    Key([mod, "shift"], "Tab", lazy.layout.client_to_next()),
    Key([mod, "shift"], "space", lazy.layout.rotate()),
    Key([mod, "shift"], "Return", lazy.layout.toggle_split()),
    Key([mod], "space", lazy.next_layout()),

    Key([mod], "t", lazy.window.toggle_floating()),

    #Key([mod], "w", lazy.to_screen(0)),
    #Key([mod, "shift"], "w", lazy.function(move_window_to_screen(0))),
    #Key([mod], "e", lazy.to_screen(1)),
    #Key([mod, "shift"], "e", lazy.function(move_window_to_screen(1))),

    Key([mod], "Return", lazy.spawn("gnome-terminal")),
    
    # dmenu-like menu ;)
    Key([mod], "p", lazy.spawn("rofi -show run")),

    # kill current window
    Key([mod], "F4", lazy.window.kill()),

    Key([mod, "control"], "r", lazy.restart()),
    Key([mod, "control"], "q", lazy.shutdown()),
    
    # interact with prompts
    Key([mod], "r", lazy.spawncmd()),
    Key([mod], "g", lazy.switchgroup()),
    
    # changing volume the old fashioned way
    Key([mod], "equal", lazy.spawn("amixer -c 0 -q set Master 2dB+")),
    Key([mod], "minus", lazy.spawn("amixer -c 0 -q set Master 2dB-")),
    
    # ake screenshot current window;
    # you can drag and draw the region to snap (use mouse)
    Key([mod], "Print",
        lazy.spawn("scrot '%Y-%m-%d_$wx$h_scrot.png' -e 'mv $f ~/' -b -s -z")),
    
    Key(['mod4'], 'space', lazy.function(next_keyboard())),
    Key(['mod4'], '1', lazy.display_kb()),

    # for Tile layout
    Key([mod, "shift"], "i", lazy.layout.increase_ratio()),
    Key([mod, "shift"], "d", lazy.layout.decrease_ratio()),
]


mouse = [
    Click([mod], "Button1", lazy.window.bring_to_front()),
    Drag([mod], "Button1", lazy.window.set_position_floating(),
         start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(),
         start=lazy.window.get_size()),
]


################################################################################

FIREFOX     = u"\uf269"
CODING      = u"\uf044"
FM          = u"\uf07b"
TERMINAL    = u"\uf120"
JABBER      = u"\uf086"
MEDIAPLAYER = u"\uf04b"
OTHER       = u"\uf074"

group_names = [
    (
        FIREFOX,
        {
            'layout': 'max',
            'spawn': ['firefox']
        }
    ),
    (
        CODING,
        {
            'layout': 'max',
            'spawn': [
                'gedit %s' % os.path.expanduser('~/.config/qtile/config.py')
            ]
        }
    ),
    (
        FM,
        {
            'layout': 'max',
            'spawn': ['nemo']
        }
    ),
    (
        TERMINAL,
        {
            'layout': 'max',
            'spawn': ['xterm']
        }
    ),
    (
        JABBER,
        {
            'layout': 'max',
            'spawn': ['gajim']
        }
    ),
    (MEDIAPLAYER, {
        'layout': 'max',
        'spawn': ['vlc -L -Z --open /home/szia/Музыка/Хелависа/']
    }),
    (OTHER, {'layout': 'max'}),
]

for n, (i, o) in enumerate(group_names):
    group_names[n] = str(n + 1) + ": " + i, o

groups = [Group(name, **kwargs) for name, kwargs in group_names]

################################################################################


for i, (name, kwargs) in enumerate(group_names, 1):
    keys.append(Key([mod], str(i), lazy.group[name].toscreen()))
    keys.append(Key([mod, "shift"], str(i), lazy.window.togroup(name)))

layouts = [
    layout.Stack(stacks=2, border_normal="#222222"),
    layout.Tile(),
    layout.Max(),
    layout.TreeTab(),
    
]


def get_bottom_bar():
    return bar.Bar([
        widget.Image(filename=os.path.expanduser('~/.config/qtile/logo.png')),
        widget.GroupBox(
            active=background,
            background='#000000',
            borderwidth=2,
            font=font2groups,
            fontshadow='#AA0000',
            fontsize=fontsize,
            highlight_method='block',
            inactive='222222',
            margin_x=5,
            margin_y=2,
            opacity=0.5,
            padding=1,
            rounded=False,
            urgent_border=alert
            ),
        widget.CurrentLayout(**font_params),
        widget.Sep(foreground='#000000'),
        widget.Prompt(),
        widget.Spacer(),
        KeyboardLayout,
        widget.Sep(foreground='#000000'),
        widget.CPUGraph(
            background='#FFFFFF',
            border_color='#000000',
            frequency=2,
            graph_color='#FF0000',
            line_width=1,
        ),
        widget.NetGraph(
            bandwidth_type='down',
            background='#FFFFFF',
            border_color='#000000',
            frequency=2,
            graph_color='#0000FF',
            interface='auto',
            line_width=1,
        ),
        widget.Sep(foreground='#000000'),
        widget.Volume(
            emoji=False,
            mute_command=['amixer', '-q', 'set', 'Master', 'toggle'],
            background='#FFFFFF',
            foreground='#000000'),
        #widget.Clipboard(timeout=100),
        widget.Sep(foreground='#000000'),
        widget.Systray(icon_size=16, background='#FFFFFF'),
        widget.Sep(foreground='#000000'),
        widget.Clock(format='%c', **font_params),
    ], 24)

def get_top_bar():
    return bar.Bar([
        widget.WindowName(**font_params),
        widget.Sep(foreground='#000000'),
        widget.Sep(foreground='#000000'),
        widget.LaunchBar([
            ('Gedit', 'gedit', 'text editor'),
            ('Empathy', 'empathy', 'Messenger'),
            ('Logout', 'qshell:self.qtile.cmd_shutdown()', 'logout from qtile'),
            ],
            #default_icon='/usr/share/icons/Mint-X/mimetypes/16/application-x-executable.png',
        )
    ], 20)

screens = [
    Screen(
        top=get_top_bar(),
        bottom=get_bottom_bar()
    ),
]


@hook.subscribe.startup_once
def autostart():
    subprocess.Popen(['nm-applet'])
    #lazy.spawn('setxkbmap -layout us,ru -option grp:ctrl_shift_toggle,grp_led:scroll,compose:rctrl')


################################################################################

patterns = [
    '/usr/share/backgrounds/*.jpg',
    '/usr/share/backgrounds/*/*.jpg',
]
wallpapers = []
for i in patterns:
    wallpapers.extend(glob(i))


def wallpaper():
    while True:
        subprocess.call(["feh", "--bg-fill", choice(wallpapers)])
        sleep(300)


@hook.subscribe.startup
def startup():
    from threading import Thread
    Thread(target=wallpaper).start()

################################################################################


@hook.subscribe.client_new
def client_new(c):
    if c.name in ('xterm', 'gnome-terminal'):
        c.togroup('TERMINAL')


def main(qtile):
    ''' This function is called when Qtile starts. '''
    pass

