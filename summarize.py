from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer

from collections import Counter
import re


def generate_notes(transcript):

    # -----------------------------
    # SUMMARY
    # -----------------------------
    parser = PlaintextParser.from_string(
        transcript,
        Tokenizer("english")
    )

    summarizer = LsaSummarizer()

    summary_sentences = summarizer(
        parser.document,
        5
    )

    summary_text = ""

    for sentence in summary_sentences:
        summary_text += f"• {sentence}\n\n"

    # -----------------------------
    # KEY CONCEPTS FROM TRANSCRIPT
    # -----------------------------
    words = re.findall(
        r'\b[a-zA-Z]{4,}\b',
        transcript.lower()
    )

    stop_words = {
        "this","that","with","from","have","will",
        "they","them","their","there","about",
        "today","video","into","were","been",
        "being","than","what","when","where",
        "which","while","your","these","those",
        "would","could","should","system"
    }

    filtered_words = [
        word for word in words
        if word not in stop_words
    ]

    common_words = Counter(
        filtered_words
    ).most_common(6)

    key_concepts = ""

    for word, count in common_words:
        key_concepts += f"• {word.title()}\n"

    # -----------------------------
    # TAKEAWAYS
    # -----------------------------
    takeaways = ""

    for word, count in common_words[:4]:
        takeaways += (
            f"• Learn more about {word.title()}\n"
        )

    # -----------------------------
    # FINAL NOTES
    # -----------------------------
    notes = f"""
📌 SUMMARY
────────────────────────

{summary_text}

📖 KEY CONCEPTS
────────────────────────

{key_concepts}

✅ IMPORTANT TAKEAWAYS
────────────────────────

{takeaways}
"""

    return notes