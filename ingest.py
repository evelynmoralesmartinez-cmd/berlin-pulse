from pathlib import Path

import chromadb
import ollama
import pandas as pd

DOCS_DIR = Path("docs")
PLACES_CSV = DOCS_DIR / "places.csv"
CHROMA_DIR = "chroma_db"
COLLECTION_NAME = "berlin_pulse"
EMBEDDING_MODEL = "nomic-embed-text"
DOCUMENT_PREFIX = "search_document: "  # nomic-embed-text expects this prefix for documents
QUERY_PREFIX = "search_query: "  # ...and this one for questions


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


def embed_texts(texts: list[str], prefix: str) -> list[list[float]]:
    """Turn a list of texts into embeddings with the local Ollama model."""
    response = ollama.embed(model=EMBEDDING_MODEL, input=[prefix + text for text in texts])
    return response["embeddings"]


def build_vector_db(chunks: list[dict]):
    """Store all chunks and their embeddings in a fresh ChromaDB collection."""
    client = chromadb.PersistentClient(path=CHROMA_DIR)
    existing_names = [collection.name for collection in client.list_collections()]
    if COLLECTION_NAME in existing_names:
        client.delete_collection(COLLECTION_NAME)  # start fresh, so re-running never duplicates chunks
    collection = client.create_collection(
        name=COLLECTION_NAME, metadata={"hnsw:space": "cosine"}
    )
    texts = [chunk["text"] for chunk in chunks]
    collection.add(
        ids=[f"chunk_{i}" for i in range(len(chunks))],
        documents=texts,
        embeddings=embed_texts(texts, DOCUMENT_PREFIX),
        metadatas=[{"source": chunk["source"]} for chunk in chunks],
    )
    return collection


if __name__ == "__main__":
    all_chunks = load_text_chunks(DOCS_DIR) + load_place_chunks(PLACES_CSV)
    print(f"Total chunks: {len(all_chunks)}")

    collection = build_vector_db(all_chunks)
    print(f"Chunks stored in ChromaDB: {collection.count()}")

    test_question = "What typical food should I try in Berlin?"
    question_embedding = embed_texts([test_question], QUERY_PREFIX)[0]
    results = collection.query(query_embeddings=[question_embedding], n_results=3)

    print(f"\nTest question: {test_question}")
    for text, metadata in zip(results["documents"][0], results["metadatas"][0]):
        print(f"- [{metadata['source']}] {text[:90]}...")
