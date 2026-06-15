from flask import send_file
from flask import Flask, render_template, request, send_file, session
from extract_audio import extract_audio
from transcribe import transcribe_audio
from summarize import generate_notes
from youtube_downloader import download_youtube_video
from generate_pdf import create_pdf
#from quiz_generator import generate_quiz
#from quiz_test_generator import generate_quiz_test
import os

app = Flask(__name__)
app.secret_key = "juveriya_video_notes_project"

UPLOAD_FOLDER = "uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/upload", methods=["POST"])
def upload():

    youtube_url = request.form.get("youtube_url")

    # ==========================
    # YOUTUBE URL CASE
    # ==========================
    if youtube_url and youtube_url.strip():

        filepath = download_youtube_video(youtube_url)

        print("Downloaded File:", filepath)

        if not os.path.exists(filepath):
            return "Downloaded file not found!"

        print("File Size:", os.path.getsize(filepath))

        if os.path.getsize(filepath) == 0:
            return "Downloaded audio is empty!"

        transcript, timestamps = transcribe_audio(filepath)

    # ==========================
    # VIDEO UPLOAD CASE
    # ==========================
    else:

        video = request.files.get("video")

        if not video or video.filename == "":
            return "Please upload a video or provide a YouTube URL"

        filepath = os.path.join(
            app.config["UPLOAD_FOLDER"],
            video.filename
        )

        video.save(filepath)

        # Extract audio from uploaded video
        audio_path = extract_audio(filepath)

        print("Audio Path:", audio_path)
        print("Exists:", os.path.exists(audio_path))
        print("Size:", os.path.getsize(audio_path))

        transcript, timestamps = transcribe_audio(audio_path)

    # Generate Notes
    notes = generate_notes(transcript)

    session["notes"] = notes
    session["transcript"] = transcript
    session["timestamps"] = timestamps

    create_pdf(notes, transcript)
    word_count = len(transcript.split())

    return render_template(
    "result.html",
    transcript=transcript,
    notes=notes,
    timestamps=timestamps,
    word_count=word_count
)

@app.route("/download")
def download_pdf():
    return send_file(
        "uploads/notes.pdf",
        as_attachment=True
    )
@app.route("/submit_quiz", methods=["POST"])
def submit_quiz():

    score = 0

    total = len(
        [key for key in request.form.keys()
         if key.startswith("correct")]
    )

    for i in range(1, total + 1):

        user_answer = request.form.get(f"q{i}")
        correct_answer = request.form.get(f"correct{i}")

        if user_answer == correct_answer:
            score += 1

    return render_template(
        "result.html",
        notes=session.get("notes"),
        transcript=session.get("transcript"),
        timestamps=session.get("timestamps"),
        #quiz=session.get("quiz"),
        #quiz_test=session.get("quiz_test"),
        score=score,
        total=total
    )
if __name__ == "__main__":
    app.run(debug=True)