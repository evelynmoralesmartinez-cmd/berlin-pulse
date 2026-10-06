# Berlin Pulse – The pulse of Berlin

Berlin Pulse is a local AI travel guide for tourists. It combines a Streamlit map of Berlin's
main sights with a chat that answers questions using a curated knowledge base and a local LLM
(Ollama). Everything runs on your own computer: no paid APIs, and no data leaves your machine.

---

## Tech stack

| Component | Tool |
|---|---|
| Frontend | Streamlit |
| LLM | Ollama – `qwen3.5:2b` |
| Embeddings | Ollama – `nomic-embed-text` |
| Vector database | ChromaDB |
| Data | pandas |

---

## Knowledge base

| File | Content | Status |
|---|---|---|
| `docs/places.csv` | 37 main sights: district, category, coordinates, description (used for the map) | ✅ |
| `docs/berlin_facts.txt` | Population, currency, language, transport, best time to visit, tipping | ✅ |
| `docs/districts.txt` | One place of interest per district (12 districts) | ✅ |
| `docs/places/` | Detailed files, one per place (use `_template.txt`) | ✅ Charlottenburg Palace |
| `docs/food.txt` | Typical food and sweets | ✅ |
| `docs/kids.txt` | Activities for children | ✅ |
| `docs/where_to_stay.txt` | Neighbourhoods to stay in | ✅ |
| `docs/safety.txt` | Safety tips and emergency numbers | ✅ |

---

## How to write the documents

1. **Lines that start with `#` are instructions.** The app ignores them.
2. **One idea per paragraph, separated by an empty line.** Each paragraph becomes a *chunk*.
3. **Each paragraph must make sense on its own.** Repeat the place name and "Berlin" in each
   paragraph, because the retrieval step only sees the chunk, not the whole document.
4. **Write in English.** The app, the users and the demo are in English.
5. **Fact-check everything.** If a fact is wrong here, the app will repeat it with confidence.

---

## Tip: coordinates for `places.csv`

In Google Maps, right-click on a place → the first line shows the coordinates
(for example `52.5163, 13.3777`). The first number is `lat`, the second is `lon`.

---

## Screenshots

![Berlin Pulse – screenshot 1](screenshots/berlin-pulse-01.png)

![Berlin Pulse – screenshot 2](screenshots/berlin-pulse-02.png)

![Berlin Pulse – screenshot 3](screenshots/berlin-pulse-03.png)