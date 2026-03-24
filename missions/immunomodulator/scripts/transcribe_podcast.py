"""
Transcribe NotebookLM podcasts via OpenAI Whisper (local, no API).
Outputs plain text (no timestamps) to artefacts/podcasts/.
"""

import whisper
import sys
import os

BASE = r"C:\Users\reyno\scisense\missions\immunomodulator"
PODCAST_DIR = os.path.join(BASE, "artefacts", "podcasts")


def transcribe(audio_path, model_name="medium", language="fr"):
    """Transcribe an audio file and return plain text."""
    print(f"Loading Whisper model '{model_name}'...")
    model = whisper.load_model(model_name)

    print(f"Transcribing: {os.path.basename(audio_path)}")
    print(f"Language: {language}")
    result = model.transcribe(audio_path, language=language, verbose=False)

    return result["text"]


def main():
    if len(sys.argv) > 1:
        audio_path = sys.argv[1]
    else:
        # Default: first .m4a in podcasts dir
        files = [f for f in os.listdir(PODCAST_DIR) if f.endswith((".m4a", ".mp3", ".wav"))]
        if not files:
            print("No audio files found in", PODCAST_DIR)
            sys.exit(1)
        audio_path = os.path.join(PODCAST_DIR, files[0])

    if not os.path.exists(audio_path):
        print(f"File not found: {audio_path}")
        sys.exit(1)

    model_name = sys.argv[2] if len(sys.argv) > 2 else "medium"
    language = sys.argv[3] if len(sys.argv) > 3 else "fr"

    text = transcribe(audio_path, model_name, language)

    # Output path: same name, .txt extension
    base_name = os.path.splitext(os.path.basename(audio_path))[0]
    out_path = os.path.join(PODCAST_DIR, f"{base_name}_transcript.txt")

    with open(out_path, "w", encoding="utf-8") as f:
        f.write(text)

    print(f"\nSaved transcript: {out_path}")
    print(f"Length: {len(text)} chars, ~{len(text.split())} words")


if __name__ == "__main__":
    main()
