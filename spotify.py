import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from spotipy.oauth2 import SpotifyOAuth
import matplotlib.pyplot as plt
import tekore as tk



SPOTIPY_CLIENT_ID="5343e166b6574443b09079a052114047"
SPOTIPY_CLIENT_SECRET="f742e42622804c29ab33a3cc52022225"
SPOTIPY_REDIRECT_URI="https://localhost:8888/callback"

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=SPOTIPY_CLIENT_ID,
                                               client_secret=SPOTIPY_CLIENT_SECRET,
                                               redirect_uri=SPOTIPY_REDIRECT_URI,
                                               scope="playlist-read-private"))

# client_id = "5343e166b6574443b09079a052114047"
# client_secret = "f742e42622804c29ab33a3cc52022225"
# app_token = tk.request_client_token(client_id, client_secret)

def batch_by_100s(data):
    # batch data into groups of 100
    batched = []
    for i in range(0, len(data), 100):
        chunk = data[i:i + 100]
        batched.append(chunk)
    return batched

# def track_audio_features(track_id):
#     return sp.audio_features([track_id])

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









playlist_name = input("Enter playlist name: ")
playlist = get_playlist_from_playlist_name(playlist_name)
tracks = get_playlist_tracks(playlist)
track_ids = get_track_ids_from_tracks(tracks)
# batched_track_ids = batch_by_100s(track_ids)
playlist_audio_features = get_audio_features_for_track_ids(track_ids)
print(playlist_audio_features)
# graph_audio_features(playlist_audio_features, 'energy', 'tempo')



# track_id = input("Enter track id: ")
# print(track_audio_features(track_id))

