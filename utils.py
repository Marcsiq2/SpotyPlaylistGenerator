import csv
import sys
import os
import re
import spotipy
import spotipy.util as util
from utils import *
from spotipy.oauth2 import SpotifyClientCredentials

scope = 'playlist-modify-public'

def authenticate(username):
    token = util.prompt_for_user_token(username, scope)
    sp = spotipy.Spotify(auth=token)
    return sp

def get_playlists(sp, username):
    plays = [pl['name'] for pl in sp.user_playlists(username)['items'] if pl['owner']['id'] == username]
    return plays


def get_playlist_id(sp, username, name):
    for pl in sp.user_playlists(username)['items']:
        if name == pl['name']:
            return pl['id'], pl['external_urls']
    return False, False

def save_to_txt(data, playlist_name, num):
    filename = os.getcwd() + "/" + playlist_name.replace(' ','_') + '.txt'
    print "Saving playlist names to --> " + filename
    thefile = open(filename, 'w')
    for k, item in enumerate(data):
        if num:
            thefile.write("%i - %s\n" % (k, item.encode('utf-8')))
        else:
            thefile.write("%s\n" % item.encode('utf-8'))
    thefile.close()
    print "Done!"

def parse_song_file(sp, song_file):
    print "Searching for the songs in spotify..."
    content = song_file.readlines()
    data = [x.strip() for x in content] 
    len_data = 0
    tracks = []
    for row in list(set(data)):
        query = re.sub(r"[^\w\s]", '', row)
        len_data+=1
        search = sp.search(query)['tracks']['items']
        if len(search) > 0:
            tracks.append(search[0]['id'])
        else:
            print ">>> Song not found: " + query 
            
    print 'Number of query songs: ' + str(len_data)
    print 'Number of found songs: ' + str(len(tracks))
    return tracks