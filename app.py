import re

import chromadb
import ollama
import pandas as pd
import streamlit as st

from ingest import CHROMA_DIR, COLLECTION_NAME, PLACES_CSV, QUERY_PREFIX, embed_texts

LLM_MODEL = "qwen3.5:2b"
N_RESULTS = 4  # how many chunks to retrieve for each question (the "k")

SYSTEM_PROMPT = (
    "You are Berlin Pulse, a friendly local guide for tourists in Berlin. "
    "Answer ONLY with information from the context you receive. "
    "If the context does not contain the answer, say that you don't have that information. "
    "Answer in English, in a short and clear way."
)


@st.cache_resource
def get_collection():
    """Open the ChromaDB collection created by ingest.py."""
    client = chromadb.PersistentClient(path=CHROMA_DIR)
    return client.get_collection(COLLECTION_NAME)


@st.cache_data
def load_places() -> pd.DataFrame:
    """Load the places for the map."""
    return pd.read_csv(PLACES_CSV)


def retrieve(question: str) -> tuple[list[str], list[str]]:
    """Find the chunks closest in meaning to the question (Retrieval)."""
    question_embedding = embed_texts([question], QUERY_PREFIX)[0]
    results = get_collection().query(
        query_embeddings=[question_embedding], n_results=N_RESULTS
    )
    texts = results["documents"][0]
    sources = [metadata["source"] for metadata in results["metadatas"][0]]
    return texts, sources


def generate_answer(question: str, context_texts: list[str]) -> str:
    """Ask the local LLM to answer using only the retrieved context (Generation)."""
    context = "\n\n".join(context_texts)
    response = ollama.chat(
        model=LLM_MODEL,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": f"Context:\n{context}\n\nQuestion: {question}"},
        ],
    )
    answer = response["message"]["content"]
    # some models write their reasoning between <think> tags: hide it from the user
    return re.sub(r"<think>.*?</think>", "", answer, flags=re.DOTALL).strip()


# ---------- Page ----------
st.set_page_config(page_title="Berlin Pulse", page_icon="🐻", layout="wide")
st.title("🐻 Berlin Pulse")
st.caption("The pulse of Berlin – a local travel guide.")

try:
    get_collection()
except Exception:  # the database does not exist yet
    st.error("The knowledge base was not found. Run `python ingest.py` first.")
    st.stop()

# ---------- Map ----------
st.subheader("Main sights")
places_df = load_places()
st.map(places_df, latitude="lat", longitude="lon")

# ---------- Chat ----------
st.subheader("Ask Berlin Pulse")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if message.get("sources"):
            st.caption("Sources: " + ", ".join(message["sources"]))

question = st.chat_input("Ask about Berlin: sights, food, transport, safety...")

if question:
    st.session_state.messages.append({"role": "user", "content": question})
    with st.chat_message("user"):
        st.markdown(question)

    with st.chat_message("assistant"):
        with st.spinner("Searching the Berlin knowledge base..."):
            context_texts, sources = retrieve(question)
            answer = generate_answer(question, context_texts)
        unique_sources = sorted(set(sources))
        st.markdown(answer)
        st.caption("Sources: " + ", ".join(unique_sources))

    st.session_state.messages.append(
        {"role": "assistant", "content": answer, "sources": unique_sources}
    )
