import spotify
import csv


def data_to_csv():
    # get datasets
    country = spotify.get_playlist_from_playlist_name("country")
    country_tracks = spotify.get_playlist_tracks(country)
    pop = spotify.get_playlist_from_playlist_name("pop")
    pop_tracks = spotify.get_playlist_tracks(pop)
    rap = spotify.get_playlist_from_playlist_name("rap")
    rap_tracks = spotify.get_playlist_tracks(rap)
    rock = spotify.get_playlist_from_playlist_name("rock")
    rock_tracks = spotify.get_playlist_tracks(rock)

    audio_features_for_country = spotify.get_audio_features_for_track_ids(
        spotify.get_track_ids_from_tracks(country_tracks))
    audio_features_for_pop = spotify.get_audio_features_for_track_ids(
        spotify.get_track_ids_from_tracks(pop_tracks))
    audio_features_for_rap = spotify.get_audio_features_for_track_ids(
        spotify.get_track_ids_from_tracks(rap_tracks))
    audio_features_for_rock = spotify.get_audio_features_for_track_ids(
        spotify.get_track_ids_from_tracks(rock_tracks))

    field_names = ['danceability', 'energy', 'key', 'loudness', 'mode', 'speechiness', 'acousticness',
                   'instrumentalness', 'liveness', 'valence', 'tempo', 'id', 'duration_ms', 'time_signature',
                   'type', 'uri', 'analysis_url', 'track_href'
                   ]

    with open('country.csv', 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=field_names)
        writer.writeheader()
        writer.writerows(audio_features_for_country)

    with open('pop.csv', 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=field_names)
        writer.writeheader()
        writer.writerows(audio_features_for_pop)

    with open('rap.csv', 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=field_names)
        writer.writeheader()
        writer.writerows(audio_features_for_rap)

    with open('rock.csv', 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=field_names)
        writer.writeheader()
        writer.writerows(audio_features_for_rock)

data_to_csv()
