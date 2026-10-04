# Berlin Pulse – The pulse of Berlin

Berlin Pulse is a local AI travel guide for tourists. It combines a Streamlit map of Berlin's
main sights with a chat that answers questions using a curated knowledge base and a local LLM
(Ollama). Everything runs on your own computer: no paid APIs, and no data leaves your machine.

*(Berlin Pulse es una guía de viaje con IA local para turistas. Combina un mapa en Streamlit con
los principales lugares de Berlín y un chat que responde preguntas usando una base de conocimiento
curada y un LLM local (Ollama). Todo funciona en tu propio computador: sin APIs pagadas y sin que
los datos salgan de tu máquina.)*

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

## Knowledge base / Base de conocimiento

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

## How to write the documents / Cómo escribir los documentos

1. **Lines that start with `#` are instructions.** The app ignores them.
   *(Las líneas que empiezan con `#` son instrucciones. La app las ignora.)*

2. **One idea per paragraph, separated by an empty line.** Each paragraph becomes a *chunk*.
   *(Una idea por párrafo, separados por una línea vacía. Cada párrafo se convierte en un chunk.)*

3. **Each paragraph must make sense on its own.** Repeat the place name and "Berlin" in each
   paragraph, because the retrieval step only sees the chunk, not the whole document.
   *(Cada párrafo debe entenderse solo. Repite el nombre del lugar y "Berlin", porque el
   retrieval solo ve el trozo, no el documento completo.)*

4. **Write in English.** The app, the users and the demo are in English.
   *(Escribe en inglés: la app, los usuarios y la demo están en inglés.)*

5. **Fact-check everything.** If a fact is wrong here, the app will repeat it with confidence.
   *(Verifica todos los datos. Si un dato está mal aquí, la app lo repetirá con seguridad.)*

---

## Tip: coordinates for `places.csv`

In Google Maps, right-click on a place → the first line shows the coordinates
(for example `52.5163, 13.3777`). The first number is `lat`, the second is `lon`.

*(En Google Maps, haz clic derecho en un lugar → la primera línea muestra las coordenadas.
El primer número es `lat` y el segundo es `lon`.)*