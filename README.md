# TripCraft AI

An agentic AI travel planner built for a GenAI course project. It plans
budget trips within India, grounded in a small destination knowledge base,
using live weather and currency tools, and checks every itinerary against
the traveller's budget and trip length before showing it.

Full write-up (architecture, tech stack, testing, evaluation) is in the
accompanying project report. This README only covers running the code.

## How it works

```
memory -> router -> [retrieve | weather | currency | skip] -> planner
       -> validate -> (loop back to planner up to 2 times on failure)
       -> save -> END
```

- **Router** — an LLM call classifies the request into one of four routes.
- **Retrieve** — ChromaDB similarity search over 10 destination guides (RAG).
- **Weather / Currency** — live calls to Open-Meteo and Frankfurter (no key needed).
- **Planner** — writes the itinerary as JSON, grounded only in retrieved
  context and tool results.
- **Validate** — a Pydantic schema check plus rule-based checks (day count,
  budget). On failure, the specific problems are sent back to the planner,
  up to 2 retries.

See `graph.py` for the full pipeline and `schemas.py` for the validator.

## 1. Run it locally

```bash
git clone <your-repo-url>
cd tripcraft-ai
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt

cp .env.example .env
# edit .env and set GROQ_API_KEY (free key: https://console.groq.com/keys)

streamlit run app.py
```

The first run downloads a small ONNX embedding model and builds the local
Chroma index in `chroma_db/` — this needs internet once, after which it's
cached.

## 2. Run the tests

```bash
pip install pytest
pytest tests/ -v
```

`tests/test_schemas.py` covers the validator (day-count mismatch, over-budget,
empty days, malformed JSON) with no API key or network needed.

## 3. Push to GitHub

```bash
git init
git add .
git commit -m "TripCraft AI: agentic travel planner"
git branch -M main
git remote add origin https://github.com/<your-username>/<your-repo>.git
git push -u origin main
```

`.gitignore` already excludes `.env` and `.streamlit/secrets.toml` — double
check neither shows up in `git status` before your first push. **Never commit
a real API key.**

## 4. Deploy on Streamlit Community Cloud (free)

1. Push the repo to GitHub (step 3).
2. Go to [share.streamlit.io](https://share.streamlit.io) and sign in with GitHub.
3. Click **New app**, pick your repo, branch `main`, main file `app.py`.
4. Under **Advanced settings -> Secrets**, paste:
   ```toml
   GROQ_API_KEY = "your_real_key_here"
   ```
5. Click **Deploy**. You'll get a public `*.streamlit.app` link — that's your
   hosted project link.

## 5. Upload to Google Drive

Zip the project folder (excluding `.env`, `chroma_db/`, and `__pycache__/`),
upload the zip (or the unzipped folder) to a Google Drive folder, then set
sharing to **Anyone with the link -> Viewer** before submitting the link.

## Project structure

```
app.py            Streamlit UI
graph.py           LangGraph pipeline (8 nodes)
schemas.py          Pydantic itinerary schema + validator
tools.py            Weather (Open-Meteo) and currency (Frankfurter) tools
retriever.py        ChromaDB setup and RAG query
prompts.py           Router and planner prompt templates
data/guides.py       10 destination guides (knowledge base)
tests/test_schemas.py Validator unit tests
requirements.txt
.env.example
.streamlit/secrets.toml.example
```

## Notes

- Swap in your own destinations in `data/guides.py` (add `coords` for the
  weather tool) if you want to extend past the 10 included here.
- The planner is told to answer only from retrieved context and tool
  results, decline unrelated requests, and never reveal its system prompt —
  see the guardrail tests in the report's Testing section.
