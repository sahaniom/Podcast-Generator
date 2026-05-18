import os
import streamlit as st

from main import main
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


# -----------------------------
# GENERATE BUTTON
# -----------------------------
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

                st.success("Podcast generated successfully!")

                # -----------------------------
                # AUDIO PLAYER
                # -----------------------------
                st.audio(final_podcast_path)

                # -----------------------------
                # DOWNLOAD BUTTON
                # -----------------------------
                with open(final_podcast_path, "rb") as f:

                    st.download_button(
                        label="Download Podcast",
                        data=f,
                        file_name=os.path.basename(final_podcast_path),
                        mime="audio/wav"
                    )

            except Exception as e:

                st.error(str(e))