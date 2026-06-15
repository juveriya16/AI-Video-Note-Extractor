import whisper
import os

# Better accuracy than tiny
model = whisper.load_model("base")

def transcribe_audio(audio_path):

    print("Audio Path:", audio_path)

    if not os.path.exists(audio_path):
        raise Exception("Audio file does not exist!")

    if os.path.getsize(audio_path) == 0:
        raise Exception("Audio file is empty!")

    # Force English transcription
    result = model.transcribe(
        audio_path,
        fp16=False,
        language="en"
    )

    transcript = result["text"]

    timestamps = []

    # Show only one timeline entry per minute
    last_minute = -1

    for seg in result["segments"]:

        current_minute = int(seg["start"] // 60)

        if current_minute != last_minute:

            timestamps.append(
                f"⏰ {current_minute:02d}:00 - {seg['text'][:120]}"
            )

            last_minute = current_minute

    return transcript, timestamps