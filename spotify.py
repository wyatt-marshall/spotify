import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from spotipy.oauth2 import SpotifyOAuth
import matplotlib.pyplot as plt
import json

SPOTIPY_CLIENT_ID = "5343e166b6574443b09079a052114047"
SPOTIPY_CLIENT_SECRET = "f742e42622804c29ab33a3cc52022225"
SPOTIPY_REDIRECT_URI = "https://localhost:8888/callback"

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=SPOTIPY_CLIENT_ID,
                                               client_secret=SPOTIPY_CLIENT_SECRET,
                                               redirect_uri=SPOTIPY_REDIRECT_URI,
                                               scope="playlist-read-private"))


def batch_by_100s(data):
    # batch data into groups of 100
    batched = []
    for i in range(0, len(data), 100):
        chunk = data[i:i + 100]
        batched.append(chunk)
    return batched


def enter_search_term():
    query = input("Search: ")
    return query


def simple_track_search(query):
    return sp.search(query)


def search_tracks(track_name: str) -> dict:
    return sp.search(track_name, type='track')['tracks']


def search_albums(album_name):
    return sp.search(album_name, type='album')['albums']


def search_artists(artist_name):
    return sp.search(artist_name, type='artist')['artists']


def resolve_artists_for_track(track):
    return [
        artist['name']
        for artist in track['artists']
    ]


def resolve_artists_for_album(album):
    return [
        artist['name']
        for artist in album['artists']
    ]


def select_track_from_search(tracks: dict) -> dict:
    while tracks['next']:
        for track in tracks['items']:
            artists = resolve_artists_for_track(track)
            print(f"Track: {track['name']} | Artist(s): {', '.join(artists)} | Album: {track['album']['name']}")
            while True:
                correct_track = input(
                    "Is this the correct track? Enter 'y' to confirm, or 'n' to view the next track (enter 'q' to quit "
                    "search): ")
                if correct_track == 'y' or correct_track == 'Y':
                    return track
                elif correct_track == 'n' or correct_track == 'N':
                    break
                elif correct_track == 'q' or correct_track == 'Q':
                    return
                print("Enter 'y' or 'n'")
        print("Loading more tracks...")
        tracks = sp.next(tracks)['tracks']
    raise Exception("Track not found")


def select_album_from_search(albums):
    while albums['next']:
        for album in albums['items']:
            artists = resolve_artists_for_album(album)
            print(f"Album: {album['name']} | Artist(s): {', '.join(artists)} | Type: {album['album_type']}")
            while True:
                correct_album = input(
                    "Is this the correct album? Enter 'y' to confirm, or 'n' to view the next album (enter 'q' to quit "
                    "search): ")
                if correct_album == 'y' or correct_album == 'Y':
                    return album
                elif correct_album == 'n' or correct_album == 'N':
                    break
                elif correct_album == 'q' or correct_album == 'Q':
                    return
                print("Enter 'y' or 'n'")
        print("Loading more albums...")
        albums = sp.next(albums)['albums']
    raise Exception("Album not found")


def select_artist_from_search(artists):
    while artists['next']:
        for artist in artists['items']:
            print(f"Artist: {artist['name']}")
            while True:
                correct_artist = input(
                    "Is this the correct artist? Enter 'y' to confirm, or 'n' to view the next artist (enter 'q' to quit "
                    "search): ")
                if correct_artist == 'y' or correct_artist == 'Y':
                    return artist
                elif correct_artist == 'n' or correct_artist == 'N':
                    break
                elif correct_artist == 'q' or correct_artist == 'Q':
                    return
                print("Enter 'y' or 'n'")
        print("Loading more artists...")
        artists = sp.next(artists)['artists']
    raise Exception("Artist not found")


def track_audio_features(track_id):
    return sp.audio_features([track_id])


def get_playlist_from_playlist_name(playlist_name: str) -> str:
    playlists = sp.current_user_playlists()
    playlist_id = ""
    for item in playlists["items"]:
        if item["name"] == playlist_name:
            playlist_id = item['id']
    if playlist_id == "":
        raise Exception(f"Playlist with name {playlist_name} not found.")
    return sp.playlist(playlist_id)


def get_playlist_tracks(playlist):
    results = sp.playlist_tracks(playlist_id=playlist['id'])
    tracks = results['items']
    while results['next']:
        results = sp.next(results)
        tracks.extend(results['items'])
    return tracks


def get_track_id_from_track(track):
    return track['track']['id']


def get_track_ids_from_tracks(tracks):
    return [
        track['track']['id']
        for track in tracks
    ]


def get_audio_features_for_track(track_id):
    return sp.audio_features(track_id)


def get_audio_features_for_track_ids(track_ids):
    #     audio_features() only accepts at most 100 track ids, so we need to batch
    batched_track_ids = batch_by_100s(track_ids)
    audio_features = []
    for batch in batched_track_ids:
        audio_features.extend(sp.audio_features(batch))
    return audio_features


def graph_audio_features(audio_features_list, x_axis, y_axis):
    x = [
        track[x_axis]
        for track in audio_features_list
    ]
    y = [
        track[y_axis]
        for track in audio_features_list
    ]
    plt.scatter(x, y, s=10, alpha=.8)
    plt.xlabel(x_axis)
    plt.ylabel(y_axis)
    plt.title(f"Displaying {x_axis} vs. {y_axis}")
    plt.show()

# def track_similarity(track1, track2):
#     """
#     given two tracks, return similarity value given comparison of tracks audio_features
#     :param track1: track object
#     :param track2: track object
#     :return: float
#     """
#     track1_id = get_track_id_from_track(track1)
#     track2_id = get_track_id_from_track(track2)
#     audio_features = sp.audio_features([track1_id, track2_id])
#     comparison = audio_features[0]
#     for feature in audio_features[0]:
#         if feature in ['danceability', 'energy', ]
#             comparison[feature] = abs(audio_features[0][feature] - audio_features[1][feature])

# albums = search_albums(enter_search_term())
# album = select_album_from_search(albums)
# print(json.dumps(album, indent=4))

# t = search_tracks(search)
# t0 = select_track_from_search(t)
# print(json.dumps(t0, indent=4))
