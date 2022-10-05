import genre_classification
import spotify
import tags
import numpy as np


def process_audio_features(audio_features):
    cleaned_features = {}
    for feature in audio_features.keys():
        if feature in ['key', 'loudness', 'mode', 'tempo', 'id', 'duration_ms', 'time_signature', 'type', 'uri',
                       'analysis_url',
                       'track_href']:
            pass
        else:
            cleaned_features[feature] = audio_features[feature]
    return [
        value
        for value in cleaned_features.values()
    ]


def predict_song():
    track_name = input("Track name: ")
    results = spotify.search_tracks(track_name)
    track_id = spotify.select_track_from_search(results)['id']
    audio_features = process_audio_features(spotify.get_audio_features_for_track(track_id)[0])
    mlp, svm = genre_classification.main()
    prediction = mlp.predict([audio_features])
    return tags.int_to_primary_tags_map[prediction[0]]


def main():
    prediction = predict_song()
    print('Prediction: ', prediction)


if __name__ == '__main__':
    main()
