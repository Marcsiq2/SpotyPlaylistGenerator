# shows a user's playlists (need to be authenticated via oauth)
import argparse
from utils import *




def main(username, playlist_name, num):
    sp = authenticate(username)
    pid, puri = get_playlist_id(sp, username, playlist_name)
    if pid:
        print "Playlist exists, getting songs..."
        tracks = [t['track']['name'] +" - "+ t['track']['artists'][0]['name'] for t in sp.user_playlist_tracks(username, pid)['items']]
        save_to_txt(tracks, playlist_name, num)
        
    else:
        print "Playlist \"" + playlist_name + "\" doesn't exist!"


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Playlist generator')

    parser.add_argument('username', metavar='username', type=str,
                    help='Your spotify username')

    parser.add_argument('playlist', metavar='playlist', type=str,
                    help='Playlist name')

    parser.add_argument('-n', dest='num', action='store_const',
                    const=True, default=False,
                    help='Add numeration to tracks')

    args = parser.parse_args()
    main(args.username, args.playlist, args.num)

    
