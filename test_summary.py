from transcribe import transcribe_audio
from summarize import generate_notes

# Convert audio to text
transcript = transcribe_audio("uploads/audio.wav")

print("Transcript Generated!")

# Generate AI notes
notes = generate_notes(transcript)

print("\nAI Notes:\n")
print(notes)