from pathlib import Path

import pandas as pd

DOCS_DIR = Path("docs")
PLACES_CSV = DOCS_DIR / "places.csv"


def load_text_chunks(docs_dir: Path) -> list[dict]:
    """Read every .txt file in docs/ and split it into paragraph chunks."""
    chunks = []
    for file_path in sorted(docs_dir.rglob("*.txt")):
        if file_path.name.startswith("_"):
            continue  # skip templates like _template.txt
        text = file_path.read_text(encoding="utf-8")
        lines = [line for line in text.splitlines() if not line.startswith("#")]
        clean_text = "\n".join(lines)
        paragraphs = [p.strip() for p in clean_text.split("\n\n") if p.strip()]
        for paragraph in paragraphs:
            chunks.append({"text": paragraph, "source": file_path.name})
    return chunks


def load_place_chunks(csv_path: Path) -> list[dict]:
    """Turn each row of places.csv into one text chunk."""
    places_df = pd.read_csv(csv_path)
    chunks = []
    for _, row in places_df.iterrows():
        text = (
            f"{row['name']} (district: {row['district']}, category: {row['category']}): "
            f"{row['short_description']}"
        )
        chunks.append({"text": text, "source": csv_path.name})
    return chunks


if __name__ == "__main__":
    text_chunks = load_text_chunks(DOCS_DIR)
    place_chunks = load_place_chunks(PLACES_CSV)
    all_chunks = text_chunks + place_chunks

    print(f"Chunks from .txt files: {len(text_chunks)}")
    print(f"Chunks from places.csv: {len(place_chunks)}")
    print(f"Total chunks: {len(all_chunks)}")
    print("Example place chunk:", place_chunks[0])
