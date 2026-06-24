import os
import streamlit as st

from main import main, generate_summary_audio
from config import SUPPORTED_LANGUAGES


st.set_page_config(
    page_title="AI Podcast Generator",
    layout="wide"
)


st.title("🎙️ AI Podcast Generator")

st.markdown(
    """
Generate multilingual AI podcasts from YouTube videos.
"""
)


# -----------------------------
# INPUTS
# -----------------------------
youtube_url = st.text_input(
    "Enter YouTube URL"
)

target_language = st.selectbox(
    "Select Language",
    SUPPORTED_LANGUAGES
)


if "summary_url" not in st.session_state:
    st.session_state.summary_url = None

if "summary_language" not in st.session_state:
    st.session_state.summary_language = None

if "summary_audio_path" not in st.session_state:
    st.session_state.summary_audio_path = None

if "podcast_path" not in st.session_state:
    st.session_state.podcast_path = None

if "podcast_language" not in st.session_state:
    st.session_state.podcast_language = None

if "podcast_url" not in st.session_state:
    st.session_state.podcast_url = None


# -----------------------------
# GENERATE BUTTONS
# -----------------------------

summary_col, podcast_col = st.columns(2, gap="small")

with summary_col:
    if st.button("Generate Summary"):

        if not youtube_url:

            st.error("Please enter a YouTube URL.")

        else:

            with st.spinner("Generating summary..."):

                try:

                    summary_audio_path = generate_summary_audio(
                        url=youtube_url,
                        target_language=target_language
                    )

                    st.session_state.summary_audio_path = summary_audio_path
                    st.session_state.summary_url = youtube_url
                    st.session_state.summary_language = target_language

                except Exception as e:

                    st.error(str(e))

with podcast_col:
    if st.button("Generate Podcast"):

        if not youtube_url:

            st.error("Please enter a YouTube URL.")

        else:

            with st.spinner("Generating podcast..."):

                try:

                    final_podcast_path = main(
                        url=youtube_url,
                        target_language=target_language
                    )

                    st.session_state.podcast_path = final_podcast_path
                    st.session_state.podcast_language = target_language
                    st.session_state.podcast_url = youtube_url

                except Exception as e:

                    st.error(str(e))
if (
    st.session_state.summary_audio_path
    and st.session_state.summary_url == youtube_url
    and st.session_state.summary_language == target_language
):

    st.success("Summary generated successfully!")

    st.subheader("🎧 Summary Audio")
    st.audio(st.session_state.summary_audio_path)

    with open(st.session_state.summary_audio_path, "rb") as f:

        st.download_button(
            label="Download Summary",
            data=f,
            file_name=os.path.basename(st.session_state.summary_audio_path),
            mime="audio/wav"
        )


if (
    st.session_state.podcast_path
    and st.session_state.podcast_language == target_language
    and st.session_state.podcast_url == youtube_url
):

    st.success("Podcast generated successfully!")

    # -----------------------------
    # AUDIO PLAYER
    # -----------------------------
    st.audio(st.session_state.podcast_path)

    # -----------------------------
    # DOWNLOAD BUTTON
    # -----------------------------
    with open(st.session_state.podcast_path, "rb") as f:

        st.download_button(
            label="Download Podcast",
            data=f,
            file_name=os.path.basename(st.session_state.podcast_path),
            mime="audio/wav"
        )