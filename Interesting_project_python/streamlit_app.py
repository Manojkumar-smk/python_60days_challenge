import streamlit as st
import requests
import streamlit.components.v1 as components

st.set_page_config(page_title="Mood Music 🎵", page_icon="🎧")
st.title("🎧 Mood-Based Music Recommender")

mood = st.selectbox("How are you feeling?", ["Happy", "Sad", "Energetic", "Relaxed"])

mood_emojis = {
    "Happy": "😄",
    "Sad": "😢",
    "Energetic": "⚡",
    "Relaxed": "🌙"
}

if st.button("Get Song"):
    st.markdown(f"## Your mood: {mood_emojis[mood]}")
    with st.spinner("Finding your perfect vibe..."):
        response = requests.get(f"http://localhost:5000/song/{mood}")
    if response.status_code == 200:
        song = response.json()
        st.success(f"🎶 {song['title']} by {song['artist']}")
        
        # Embed Spotify player
        embed_url = f"https://open.spotify.com/embed/track/{song['id']}"
        components.html(
            f"""
            <iframe src="{embed_url}" width="100%" height="150" frameborder="0" allowtransparency="true" allow="encrypted-media"></iframe>
            """,
            height=160
        )
    else:
        st.error("Oops! Couldn't find a song.")
