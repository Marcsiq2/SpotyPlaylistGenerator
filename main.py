# shows a user's playlists (need to be authenticated via oauth)
import csv
import sys
import spotipy
import argparse
import spotipy.util as util
from spotipy.oauth2 import SpotifyClientCredentials

scope = 'playlist-modify-public'

def authenticate(username):
    token = util.prompt_for_user_token(username, scope)
    sp = spotipy.Spotify(auth=token)
    return sp

def parse_song_file(sp, song_file):
    print "Searching for the songs in spotify..."
    content = song_file.readlines()
    data = [x.strip() for x in content] 
    len_data = 0
    tracks = []
    for row in list(set(data)):
        query = row
        len_data+=1
        search = sp.search(query)['tracks']['items']
        if len(search) > 0:
            tracks.append(search[0]['id'])
        else:
            print ">>> Song not found: " + query 
            
    print 'Number of query songs: ' + str(len_data)
    print 'Number of found songs: ' + str(len(tracks))
    return tracks

def get_playlist_id(sp, username, name):
    for pl in sp.user_playlists(username)['items']:
        if name == pl['name']:
            return pl['id']
    return False

def main(username, songs_file):
    sp = authenticate(username)
    
    tracks = parse_song_file(sp, songs_file)

    playlist_name = raw_input('Enter a name for your playlist: ')
    pid = get_playlist_id(sp, username, playlist_name)
    if pid:
        print "Playlist exists, just adding songs..."
        tracks_id = [t['track']['id'] for t in sp.user_playlist_tracks(username, pid)['items']]
        tracks_add = [t for t in tracks if t not in tracks_id]
        if tracks_add:
            sp.user_playlist_add_tracks(username, pid, tracks_add, position=None)
        print "Added " + str(len(tracks_add)) + " new song(s) to the playlist!"

    else:
        print "Playlist doesn't exist, creating new one..."
        sp.user_playlist_create(username,playlist_name , public=True)
        pid = get_playlist_id(sp, username, playlist_name)
        sp.user_playlist_add_tracks(username, pid, tracks, position=None)


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Playlist generator')

    parser.add_argument('username', metavar='username', type=str,
                    help='Your spotify username')

    parser.add_argument('songs_file', metavar='songs_file', type=open,
                    help='A file with a song in each line')

    args = parser.parse_args()
    main(args.username, args.songs_file)

    
