import streamlit as st
import pandas as pd
from gtts import gTTS
import os
from playsound import playsound

# Load data
@st.cache
def load_data():
    df = pd.read_csv('bhagavad-gita.xlsx')
    return df

# Function to generate and play audio
def play_audio(text):
    tts = gTTS(text=text, lang='hi')
    audio_file = "temp_explanation.mp3"
    tts.save(audio_file)
    playsound(audio_file)
    os.remove(audio_file)

# Load the data
df = load_data()

# Streamlit App UI
st.title("Bhagavad Gita Interactive App")
st.sidebar.header("Navigation")
selected_chapter = st.sidebar.selectbox("Select a Chapter", df['Chapter'].unique())

# Filter shlokas by the selected chapter
filtered_df = df[df['Chapter'] == selected_chapter]
selected_shloka = st.selectbox("Select a Shloka", filtered_df['Shloka'].unique())

# Display the selected shloka
shloka_data = filtered_df[filtered_df['Shloka'] == selected_shloka].iloc[0]
st.subheader(f"Chapter {shloka_data['Chapter']} - Shloka {shloka_data['Shloka']}")
st.text_area("Sanskrit Text", shloka_data['Sanskrit_Text'], height=150)
st.write("**Explanation in Hindi**")
st.write(shloka_data['Explanation_Hindi'])

# Explanation button with audio
if st.button("Play Explanation in Hindi"):
    play_audio(shloka_data['Explanation_Hindi'])
    st.success("Playing audio...")

# Bookmark feature
if 'bookmarked_shlokas' not in st.session_state:
    st.session_state.bookmarked_shlokas = []

if st.button("Bookmark This Shloka"):
    st.session_state.bookmarked_shlokas.append(
        (shloka_data['Chapter'], shloka_data['Shloka'])
    )
    st.success("Shloka bookmarked!")

# Display bookmarks
if st.session_state.bookmarked_shlokas:
    st.sidebar.subheader("Bookmarked Shlokas")
    for chap, shloka in st.session_state.bookmarked_shlokas:
        st.sidebar.write(f"Chapter {chap}, Shloka {shloka}")

# Daily Shloka feature
st.sidebar.subheader("Daily Shloka")
daily_shloka = df.sample(1).iloc[0]
st.sidebar.write(f"Chapter {daily_shloka['Chapter']} - Shloka {daily_shloka['Shloka']}")
st.sidebar.text_area("Daily Shloka (Sanskrit)", daily_shloka['Sanskrit_Text'], height=100)
st.sidebar.write(daily_shloka['Explanation_Hindi'])
