from moviepy import VideoFileClip
import os

def extract_audio(video_path):

    video = VideoFileClip(video_path)

    audio_path = "uploads/audio.wav"

    video.audio.write_audiofile(audio_path)

    print("Audio created:", audio_path)
    print("Audio exists:", os.path.exists(audio_path))
    print("Audio size:", os.path.getsize(audio_path))

    return audio_path