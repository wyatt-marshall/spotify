from flask import Flask, render_template
import spotify
import json

app = Flask(__name__)


@app.route("/")
def hello_world():
    return "<p>Hello, world!</p>"


@app.route("/template_test")
def template_test():
    return render_template('index.html')


# @app.route("/search_track/<track_name>")
def simple_track_search(track_name):
    result = spotify.simple_track_search(track_name)
    return result["tracks"]["items"][0]


def parse_image_from_track(track):
    images = track["album"]["images"]
    i0 = images[0]["url"]
    i1 = images[1]["url"]
    i2 = images[2]["url"]
    return i0


def parse_name_from_track(track):
    name = track["name"]
    return name


def parse_album_name_from_track(track):
    album_name = track["album"]["name"]
    return album_name


@app.route("/search_track/<track_name>")
def display(track_name):
    track = simple_track_search(track_name)
    album_art = parse_image_from_track(track)
    track_name = parse_name_from_track(track)
    album_name = parse_album_name_from_track(track)
    return render_template('index.html', album_art=album_art, track_name=track_name, album_name=album_name)
