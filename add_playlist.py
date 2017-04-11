# shows a user's playlists (need to be authenticated via oauth)
import argparse
from utils import *
scope = 'playlist-modify-public'


def main(username, songs_file):
    sp = authenticate(username)
    
    tracks = parse_song_file(sp, songs_file)

    playlist_name = raw_input('Enter a name for your playlist: ')
    pid, puri = get_playlist_id(sp, username, playlist_name)
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
        pid, puri = get_playlist_id(sp, username, playlist_name)
        sp.user_playlist_add_tracks(username, pid, tracks, position=None)
        print "Added " + str(len(tracks)) + " new song(s) to the playlist!"

    print "*** Playlist uri ***\n" + str(puri['spotify'])


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Playlist generator')

    parser.add_argument('username', metavar='username', type=str,
                    help='Your spotify username')

    parser.add_argument('songs_file', metavar='songs_file', type=open,
                    help='A file with a song in each line')

    args = parser.parse_args()
    main(args.username, args.songs_file)

    
