#!/usr/bin/env python
from __future__ import print_function
import os
import os.path
import sys
import requests
import urllib
import subprocess

MIN_WIDTH = 4000
CWD = os.path.dirname(os.path.abspath(__file__))

def plasma_wallpaper(fname):
    import dbus
    jscript = """
    var allDesktops = desktops();
    for(i = 0; i < allDesktops.length; i++) {
        d = allDesktops[i];
        d.wallpaperPlugin = "org.kde.image";
        d.currentConfigGroup = Array("Wallpaper", "org.kde.image", "General");
        d.writeConfig("Image", "file://%s")
    }"""
    bus = dbus.SessionBus()
    plasma = dbus.Interface(bus.get_object('org.kde.plasmashell', '/PlasmaShell'),
                            dbus_interface='org.kde.PlasmaShell')
    plasma.evaluateScript(jscript % fname)

d = requests.get('https://www.reddit.com/r/EarthPorn/top/.json', headers={'User-agent':'EarthWall'}).json()
for c in d['data']['children']:
    src = c['data']['preview']['images'][0]['source']
    url = src['url'].replace('&amp;', '&')
    if src['width'] >= MIN_WIDTH:
        if os.getenv('GATEWAY_INTERFACE') == 'CGI/1.1':
            print('Location:', url)
            print()
            break
        print(c['data']['title'], file=sys.stderr)
        fname = os.path.join(CWD, 'cache', c['data']['id'] + '.jpeg')
        if not os.path.exists(fname):
            print('fetching', url, '...', file=sys.stderr)
            urllib.urlretrieve(url, fname)
        subprocess.call(["feh", "--bg-fill", fname])
        plasma_wallpaper(fname)
        break
