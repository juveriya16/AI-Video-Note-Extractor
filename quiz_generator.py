from summarize import model

def generate_quiz(transcript):

    prompt = f"""
    Create 10 multiple-choice questions based on this transcript.

    Include:
    - Question
    - 4 options (A, B, C, D)
    - Correct answer

    Transcript:
    {transcript}
    """

    response = model.generate_content(prompt)

    return response.text