#!/usr/bin/env python
# coding: utf-8

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

#@hook.subscribe.startup
#def dbus_register():
#    x = os.environ['DESKTOP_AUTOSTART_ID']
#    subprocess.Popen(['dbus-send',
#                      '--session',
#                      '--print-reply=string',
#                      '--dest=org.gnome.SessionManager',
#                      '/org/gnome/SessionManager',
#                      'org.gnome.SessionManager.RegisterClient',
#                      'string:qtile',
#                      'string:' + x])

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
# COLORS

white = '#FFFFFF'
black = '#000000'
red = '#FF0000'
green = '#00FF00'
blue = '#0000FF'

################################################################################

KeyboardLayout = widget.KeyboardLayout(
    background=white,
    configured_keyboards=['us', 'ru'],
    font='Ubuntu',
    fontsize=14,
    foreground=black,
)
def next_keyboard():
    def cmd(qtile):
        return
        KeyboardLayout.next_keyboard()
    return cmd

################################################################################

font = 'PragmataProMonoW20-Regular' #'FreeMono Bold'
font2groups = 'Ubuntu Mono'#'Century Schoolbook L'
foreground = black
background = white
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
    Key([mod], "BackSpace", lazy.spawn("/home/virtuos86/PortWINE/PortWoT/data/scripts/start")),
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

    Key([mod], "Return", lazy.spawn("xfce4-terminal")),
    
    # dmenu-like menu ;)
    Key([mod], "p", lazy.spawn("rofi -show run")),

    # kill current window
    Key([mod], "F4", lazy.window.kill()),

    Key([mod, "control"], "r", lazy.restart()),
    #Key([mod, 'control'], 'l', lazy.spawn('gnome-screensaver-command -l')),
    Key([mod, 'control'], 'o', lazy.spawn('gnome-session-quit --logout --no-prompt')),
    Key([mod, 'shift', 'control'], 'o', lazy.spawn('gnome-session-quit --power-off')),
    
    # interact with prompts
    Key([mod], "r", lazy.spawncmd()),
    Key([mod], "g", lazy.switchgroup()),
    
    # changing volume the old fashioned way
    Key([mod], "equal", lazy.spawn("amixer -c 0 -q set Master 2dB+")),
    Key([mod], "minus", lazy.spawn("amixer -c 0 -q set Master 2dB-")),
    
    # ake screenshot current window;
    # you can drag and draw the region to snap (use mouse)
    Key([mod], "Print",
        lazy.spawn("scrot '%Y-%m-%d_$wx$h_scrot.png' -e 'mv $f ~/Изображения' -b -s -z")),
    
    Key(['mod4'], 'space', lazy.function(next_keyboard())),
    Key(['mod4'], '1', lazy.display_kb()),

    # for Tile layout
    Key([mod, "shift"], "i", lazy.layout.increase_ratio()),
    Key([mod, "shift"], "d", lazy.layout.decrease_ratio()),

    Key([mod], "F1", lazy.spawn("firefox57")),
]


mouse = [
    Click([mod], "Button1", lazy.window.bring_to_front()),
    Drag([mod], "Button1", lazy.window.set_position_floating(),
         start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(),
         start=lazy.window.get_size()),
]


################################################################################

FIREFOX     = u"*" # u"\uf269"
CODING      = u"/" # u"\uf044"
FM          = u"~" # u"\uf07b"
TERMINAL    = u"#" # u"\uf120"
JABBER      = u"%" # u"\uf086"
MEDIAPLAYER = u">" # u"\uf04b"
OTHER       = u"?" # u"\uf074"
TANKS       = u"^" # u"\uf1e2"
STEAM       = u"$" # u"\uf1b6"

group_names = [
    (
        FIREFOX,
        {
            'layout': 'max',
            'spawn': ['firefox57']
        }
    ),
    (
        CODING,
        {
            'layout': 'max',
            'spawn': [
                'subl %s' % os.path.expanduser('~/.config/qtile/config.py')
            ]
        }
    ),
    (
        FM,
        {
            'layout': 'max',
            'spawn': ['thunar']
        }
    ),
    (
        TERMINAL,
        {
            'layout': 'max',
            'spawn': ['xfce4-terminal']
        }
    ),
    (
        JABBER,
        {
            'layout': 'max',
            'spawn': ['telegram']
        }
    ),
    (MEDIAPLAYER, {
        'layout': 'max',
        'spawn': []#['vlc -L -Z --open /home/szia/Музыка/Хелависа/']
    }),
    (OTHER, {'layout': 'max'}),
    (TANKS, {'layout': 'max'}),
    (STEAM, {'layout': 'max'}),
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
            active=black,
            background=white,
            borderwidth=2,
            font=font2groups,
            #fontshadow='#AAAA00',
            fontsize=fontsize,
            #highlight_method='block',
            inactive=white,
            margin_x=5,
            margin_y=2,
            opacity=0.5,
            padding=1,
            rounded=False,
            urgent_border=blue
            ),
        widget.CurrentLayout(**font_params),
        #widget.Sep(foreground=white),
        #widget.Prompt(),
        widget.Spacer(),
        #KeyboardLayout,
        #widget.Sep(foreground=black),
        widget.CPUGraph(
            background=white,
            border_color=black,
            frequency=2,
            graph_color=red,
            line_width=1,
        ),
        widget.NetGraph(
            bandwidth_type='down',
            background=white,
            border_color=black,
            frequency=2,
            graph_color=blue,
            interface='auto',
            line_width=1,
        ),
        widget.Sep(foreground=white, background=white),
        widget.Volume(
            emoji=True,
            mute_command=['amixer', '-q', 'set', 'Master', 'toggle'],
            background=white,
            foreground=black),
        #widget.Clipboard(timeout=100),
        widget.Sep(foreground=white, background=white),
        widget.Systray(icon_size=20, background=white),
        widget.Sep(foreground=white, background=white),
        widget.Clock(format='%c', **font_params),
    ], 24)

def get_top_bar():
    return bar.Bar([
        widget.WindowName(background='#000000', foreground='#FFFFFF', font=font, fontsize=fontsize),
        #widget.Sep(foreground=black),
        #widget.Sep(foreground=black),
        widget.LaunchBar([
            ('/home/virtuos86/.config/qtile/st3.png', 'subl', 'Text editor'),
            ('/home/virtuos86/.config/qtile/ff.png', 'firefox57', 'Web browser'),
            ('/home/virtuos86/.config/qtile/OmegaT.png', '/usr/local/bin/omegat', 'Text translation'),
            ('/home/virtuos86/.config/qtile/sunvox.png', '/home/virtuos86/Загрузки/sunvox/sunvox/linux_x86_64/sunvox_for_old_cpu', 'Sintezator'),
            ('/home/virtuos86/.config/qtile/telegram.png', '/home/virtuos86/Загрузки/Debs/Telegram/Telegram', 'Instant messenger'),
            ('/home/virtuos86/.config/qtile/MagicISO.png', "wine '/home/virtuos86/.wine/drive_c/Program Files (x86)/MagicISO/MagicISO.exe'", 'MagicISO'),
            ('/home/virtuos86/.config/qtile/Steam.png', "/home/virtuos86/PortSteam/data/scripts/start", 'Steam'),
            #('Logout', 'qshell:self.qtile.cmd_shutdown()', 'logout from qtile'),
            ],
            #default_icon='/usr/share/icons/Mint-X/mimetypes/16/application-x-executable.png',
            #foreground=black,
            background=white
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
    subprocess.Popen(['pulseaudio', '--start', '--exit-idle-time=-1'])
    os.system('setxkbmap -layout us,ru -option grp:ctrl_shift_toggle,grp_led:scroll,compose:rwin')


################################################################################

patterns = [
    '/home/virtuos86/Изображения/Instagram/Chika/*.jpg',
    #'/usr/share/backgrounds/*.jpg',
    #'/usr/share/backgrounds/*/*.jpg',
]
wallpapers = []
for i in patterns:
    wallpapers.extend(glob(i))

keys.append(Key([mod], "F12", lazy.spawn("feh" + " --bg-fill " + choice(wallpapers))))

def wallpaper():
    global wallpapers
    if not len(wallpapers):
        return
    used_wallpapers = []
    while True:
        if not len(wallpapers):
            wallpapers = used_wallpapers
            used_wallpapers = []
        wallpaper = choice(wallpapers)
        wallpapers.remove(wallpaper)
        used_wallpapers.append(wallpaper)
        subprocess.call(["feh", "--bg-fill", wallpaper])
        sleep(30)


@hook.subscribe.startup
def startup():
    from threading import Thread
    Thread(target=wallpaper).start()

################################################################################


@hook.subscribe.client_new
def client_new(c):
    if c.name in ('xterm', 'gnome-terminal', 'xfce4-terminal'):
        c.togroup('TERMINAL')


def main(qtile):
    ''' This function is called when Qtile starts. '''
    pass

