
1. `1_get_transcript.py`: First tries to get caption via `YouTubeTranscriptApi`, if it returns null, then it downloads it's audio file and then use OpenAI's `faster-whisper` model to get it's transcript and finally prints it to console.
1. `2_get_transcript.py`: All features of `1_get_transcript.py` + it also saves the transcript in a text file named as `<video_id>.txt` in `Transcripts` folder and keeps the audio in `Audio` folder with name `<video_id>.<audio_format>` (if audio is downloaded).
