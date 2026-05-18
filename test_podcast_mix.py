from audio_processing.podcast_mixer import create_podcast


create_podcast(
    voice_path="audio/test_hindi.wav",
    output_path="outputs/final_podcast.wav",

    intro_path="assets/intro_music.mp3",
    background_path="assets/background_music.mp3",
    outro_path="assets/outro_music.mp3"
)
