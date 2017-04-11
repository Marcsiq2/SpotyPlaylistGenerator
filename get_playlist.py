# shows a user's playlists (need to be authenticated via oauth)
# -*- coding: utf-8 -*-
import argparse
from utils import *


def get_playlist(sp, playlist_name, username, num):
    pid, puri = get_playlist_id(sp, username, playlist_name)
    if pid:
        print "Playlist " + playlist_name + " exists, getting songs..."
        tracks = [t['track']['name'] +" - "+ t['track']['artists'][0]['name'] for t in sp.user_playlist_tracks(username, pid)['items']]
        save_to_txt(tracks, playlist_name, num)
        
    else:
        print "Playlist \"" + playlist_name + "\" doesn't exist!"

def main(username, num):
    sp = authenticate(username)
    print "Playlists for user "+ username + ":"
    playlists_names = get_playlists(sp, username)
    for p in playlists_names:
        print " - " + str(p.encode('utf-8'))

    playlist_name = raw_input("Please select one (or 'All'): ")
    if playlist_name=='All':
        for p in playlists_names:
            get_playlist(sp, p, username, num)
    else:
        get_playlist(sp, playlist_name, username, num)
    


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Playlist generator')

    parser.add_argument('username', metavar='username', type=str,
                    help='Your spotify username')

    parser.add_argument('-n', dest='num', action='store_const',
                    const=True, default=False,
                    help='Add numeration to tracks')

    args = parser.parse_args()
    main(args.username, args.num)

    
