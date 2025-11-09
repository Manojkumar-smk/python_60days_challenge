from flask import Flask, jsonify
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy

app = Flask(__name__)

# Spotify setup
sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials())

def get_song_by_mood(mood):
    results = sp.search(q=mood, type='track', limit=1)
    track = results['tracks']['items'][0]
    track_id = track['id']
    return {
        "title": track['name'],
        "artist": track['artists'][0]['name'],
        "url": track['external_urls']['spotify'],
        "id": track_id
    }

@app.route('/song/<mood>')
def recommend_song(mood):
    try:
        song = get_song_by_mood(mood)
        return jsonify(song)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
