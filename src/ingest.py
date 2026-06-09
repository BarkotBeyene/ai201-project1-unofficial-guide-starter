# src/ingest.py
# Loads all .txt files from data/raw/, cleans them, saves to data/cleaned/

import re
import os

RAW_DIR = "data/raw"
CLEANED_DIR = "data/cleaned"


def clean_text(text):
    # Remove HTML tags
    text = re.sub(r'<[^>]+>', '', text)

    # Decode common HTML entities
    text = re.sub(r'&amp;', '&', text)
    text = re.sub(r'&nbsp;', ' ', text)
    text = re.sub(r'&quot;', '"', text)
    text = re.sub(r'&#39;', "'", text)
    text = re.sub(r'&lt;', '<', text)
    text = re.sub(r'&gt;', '>', text)

    # Remove timestamps (e.g. [00:12:34] or 00:12 formats common in transcripts)
    text = re.sub(r'\[\d{1,2}:\d{2}(:\d{2})?\]', '', text)
    text = re.sub(r'\b\d{1,2}:\d{2}(:\d{2})?\b', '', text)

    # Remove sponsor/ad segments (common Huberman patterns)
    text = re.sub(r'(?i)this episode is brought to you by.*?(?=\n\n|\Z)', '', text, flags=re.DOTALL)
    text = re.sub(r'(?i)our sponsor.*?(?=\n\n|\Z)', '', text, flags=re.DOTALL)

    # Remove URLs
    text = re.sub(r'https?://\S+', '', text)

    # Remove repeated filler phrases common in transcripts
    text = re.sub(r'(?i)\b(um+|uh+|you know|i mean|like i said|so yeah)\b', '', text)

    # Remove references/bibliography sections
    text = re.sub(
        r'\n(References|Bibliography|Works Cited|REFERENCES|BIBLIOGRAPHY)[\s\S]*$',
        '',
        text
    )
    # Normalize whitespace (collapse multiple spaces/newlines)
    text = re.sub(r'\n{3,}', '\n\n', text)
    text = re.sub(r'[ \t]+', ' ', text)
    text = text.strip()

    return text


def ingest_all():
    os.makedirs(CLEANED_DIR, exist_ok=True)
    files = [f for f in os.listdir(RAW_DIR) if f.endswith('.txt')]

    if not files:
        print(f"No .txt files found in {RAW_DIR}")
        return

    for filename in files:
        raw_path = os.path.join(RAW_DIR, filename)
        cleaned_path = os.path.join(CLEANED_DIR, filename)

        with open(raw_path, 'r', encoding='utf-8') as f:
            raw_text = f.read()

        cleaned = clean_text(raw_text)

        with open(cleaned_path, 'w', encoding='utf-8') as f:
            f.write(cleaned)

        print(f"✓ Cleaned: {filename} ({len(raw_text)} → {len(cleaned)} chars)")

    print(f"\nDone. {len(files)} files cleaned and saved to {CLEANED_DIR}/")


if __name__ == "__main__":
    ingest_all()