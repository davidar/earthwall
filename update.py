#!/usr/bin/env python
import os.path
import requests
import urllib
import subprocess

MIN_WIDTH = 4000
CWD = os.path.dirname(os.path.abspath(__file__))

d = requests.get('https://www.reddit.com/r/EarthPorn/top/.json', headers={'User-agent':'EarthWall'}).json()
for c in d['data']['children']:
    src = c['data']['preview']['images'][0]['source']
    if src['width'] >= MIN_WIDTH:
        print(c['data']['title'])
        fname = os.path.join(CWD, 'cache', c['data']['id'] + '.jpeg')
        if not os.path.exists(fname):
            url = src['url'].replace('&amp;', '&')
            print('fetching ' + url + ' ...')
            urllib.urlretrieve(url, fname)
        subprocess.call(["feh", "--bg-fill", fname])
        break
