
import streamlit as st
import pandas as pd

# Load data function
@st.cache_data
def load_data():
    df = pd.read_excel('bhagavad_geeta.xlsx')  # Ensure correct file path and spelling
    return df

# Load the data
df = load_data()

# Streamlit App UI
st.title("Bhagavad Gita Interactive App")
st.sidebar.header("Navigation")
selected_chapter = st.sidebar.selectbox("Select a Chapter", df['Chapter'].unique())

# Filter shlokas by the selected chapter
filtered_df = df[df['Chapter'] == selected_chapter]
selected_verse = st.selectbox("Select a Verse", filtered_df['Verse'].unique())

# Display the selected verse details
verse_data = filtered_df[filtered_df['Verse'] == selected_verse].iloc[0]
st.subheader(f"Chapter {verse_data['Chapter']} - Verse {verse_data['Verse']}")
st.text_area("Sanskrit Anuvad", verse_data['Sanskrit Anuvad'], height=150)
st.write("**Hindi Anuvad**")
st.write(verse_data['Hindi Anuvad'])
st.write("**English Translation**")
st.write(verse_data['Enlgish Translation'])

# Bookmark feature
if 'bookmarked_verses' not in st.session_state:
    st.session_state.bookmarked_verses = []

if st.button("Bookmark This Verse"):
    st.session_state.bookmarked_verses.append(
        (verse_data['Chapter'], verse_data['Verse'])
    )
    st.success("Verse bookmarked!")

# Display bookmarks
if st.session_state.bookmarked_verses:
    st.sidebar.subheader("Bookmarked Verses")
    for chap, verse in st.session_state.bookmarked_verses:
        st.sidebar.write(f"Chapter {chap}, Verse {verse}")

# Daily Verse feature
st.sidebar.subheader("Daily Verse")
daily_verse = df.sample(1).iloc[0]
st.sidebar.write(f"Chapter {daily_verse['Chapter']} - Verse {daily_verse['Verse']}")
st.sidebar.text_area("Daily Verse (Sanskrit)", daily_verse['Sanskrit Anuvad'], height=100)
st.sidebar.write("**Hindi Anuvad**")
st.sidebar.write(daily_verse['Hindi Anuvad'])
st.sidebar.write("**English Translation**")
st.sidebar.write(daily_verse['Enlgish Translation'])
