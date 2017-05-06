#!/usr/bin/python

import dbus
import sys
from vagalume import lyrics
import requests
from bs4 import BeautifulSoup
import webbrowser

bus = dbus.SessionBus()

player = dbus.SessionBus().get_object("org.mpris.MediaPlayer2.spotify",
        "/org/mpris/MediaPlayer2")

#interface = dbus.Interface(player,
#        dbus_interface="org.mpris.MediaPlayer2.Player")

metadata = player.Get("org.mpris.MediaPlayer2.Player", "Metadata",
        dbus_interface="org.freedesktop.DBus.Properties")

songArtist = metadata['xesam:artist'][0]
songTitle = metadata['xesam:title']

def getMeta(artist, song):
    result = lyrics.find(artist, song)

    if result.is_not_found():
        print("Song not found")
    else:
        print(result.artist.name + " - " + result.song.name, end="\n")
        print(result.song.lyric)

def getVideo(artist, song):
    textToSearch = (artist + " " + song)
    url = ("https://www.youtube.com/results?search_query=" + textToSearch)
    r = requests.get(url)
    html = r.text
    soup = BeautifulSoup(html, "html.parser")
    for vid in soup.findAll(attrs={"class":"yt-uix-tile-link"}):
        data = []
        data.append(vid["title"].split(" - "))
        if data[0][0] == artist:
            webbrowser.open("https://www.youtube.com" + vid["href"])
            break

if len(sys.argv) > 1:
    if sys.argv[1] == "video":
        if len(sys.argv) == 2:
            getVideo(songArtist, songTitle)
        else:
            getVideo(sys.argv[2], sys.argv[3])
    else:
        getMeta(sys.argv[1], sys.argv[2])
else:
    getMeta(songArtist, songTitle)



