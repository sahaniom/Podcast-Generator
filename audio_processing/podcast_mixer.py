from pydub import AudioSegment
import os


def create_podcast(
    voice_path,
    output_path,
    intro_path=None,
    background_path=None,
    outro_path=None
):

    print("\nLoading voice audio...")

    voice = AudioSegment.from_file(voice_path)

    final_audio = AudioSegment.empty()

    # -----------------------------
    # INTRO MUSIC
    # -----------------------------
    if intro_path:

        print("Adding intro music...")

        intro = AudioSegment.from_file(intro_path)

        intro = intro.fade_in(1000).fade_out(1000)

        final_audio += intro

    # -----------------------------
    # BACKGROUND MUSIC
    # -----------------------------
    if background_path:

        print("Adding background music...")

        background = AudioSegment.from_file(background_path)

        # Reduce volume
        background = background - 25

        # Loop background if shorter
        while len(background) < len(voice):
            background += background

        background = background[:len(voice)]

        mixed_voice = voice.overlay(background)

        final_audio += mixed_voice

    else:
        final_audio += voice

    # -----------------------------
    # OUTRO MUSIC
    # -----------------------------
    if outro_path:

        print("Adding outro music...")

        outro = AudioSegment.from_file(outro_path)

        # Take only first 5 seconds
        outro = outro[:5000]

        outro = outro.fade_in(1000).fade_out(2000)

        final_audio += outro

    # -----------------------------
    # EXPORT
    # -----------------------------
    print("\nExporting final podcast...")

    output_dir = os.path.dirname(output_path)

    if output_dir:
        os.makedirs(output_dir, exist_ok=True)

    final_audio.export(
        output_path,
        format="wav"
    )

    print(f"✅ Podcast saved at: {output_path}")
