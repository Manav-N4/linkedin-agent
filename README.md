# LinkedIn Agent

A multi-agent system that researches and drafts LinkedIn posts for company pages
designed to work for any brand.

## What it does

- Takes a topic as input and classifies it by domain, content type, and angle
  (orchestrator agent)
- Researches the topic via web search, scrapes real articles, and stores
  findings as embeddings in ChromaDB (research agent)
- Finds real-world examples that support the topic (examples agent)
- Flags weaknesses in the research and examples (critic agent)
- Synthesises everything into a structured content brief (brief agent)
- Generates 5 hooks across different formats — bold claim, stat, confession,
  question, one-liner (hook agent)
- Writes 2 full post drafts in different tones — punchy and narrative (draft
  agent)
- Scores both drafts on originality, promise fulfilment, and shareability
  (writing critic agent)

User picks the best hook and draft, edits it, and publishes.

## Tech stack

- **Python 3.11** — core language
- **Ollama + gemma2:2b** — local LLM, free, no API cost
- **Pydantic** — structured output validation between agents
- **Serper API** — web search (2,500 free searches/month)
- **BeautifulSoup + requests** — web scraping
- **sentence-transformers (all-MiniLM-L6-v2)** — text embeddings
- **ChromaDB** — persistent vector store for RAG
- **FastAPI** — REST API exposing the full pipeline

## Setup

```bash
# 1. Clone the repo
git clone https://github.com/yourusername/linkedin-agent.git
cd linkedin-agent

# 2. Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Install Ollama and pull the model
# Download Ollama from ollama.com, then:
ollama pull gemma2:2b

# 5. Create your .env file
echo "SERPER_API_KEY=your_key_here" > .env
# Get a free key at serper.dev — 2,500 searches/month free

# 6. Create the data directory for ChromaDB
mkdir -p data
```

## Running

**CLI — runs the full pipeline in your terminal:**

```bash
python main.py
```

**API — starts the FastAPI server:**

```bash
./venv/bin/fastapi dev api.py
```

Then go to `http://127.0.0.1:8000/docs` to use the interactive API docs.

**Single POST endpoint:**

POST /generate Body: { "topic": "Your Topic" } Returns: { "hooks": [...],
"drafts": [...], "scores": {...} }

## Project structure

linkedin-agent/
├── agents/
│   ├── orchestrator.py        # classifies topic into domain, content type, angle
│   ├── research.py            # web search, scraping, embedding, RAG retrieval
│   ├── examples.py            # finds real-world examples supporting the topic
│   ├── critic.py              # flags weaknesses in research and examples
│   ├── brief.py               # synthesises everything into a content brief
│   ├── hook.py                # generates 5 hooks across different formats
│   ├── draft.py               # writes 2 full post drafts in different tones
│   └── writing_critic.py      # scores drafts on originality, fulfilment, shareability
├── core/
│   ├── llm.py                 # Ollama wrapper — single call_llm function
│   ├── models.py              # Pydantic models for structured agent outputs
│   └── utils.py               # shared utilities — clean_topic, strip_json_fences
├── data/
│   └── chroma/                # persistent ChromaDB storage (gitignored)
├── main.py                    # CLI entry point — runs the full pipeline
├── api.py                     # FastAPI server — POST /generate endpoint
├── requirements.txt           # all dependencies
└── .env                       # SERPER_API_KEY (gitignored)

## Status

**Built and working:**

- All 8 agents — orchestrator through writing critic
- Full pipeline via CLI (`main.py`) and REST API (`api.py`)
- Persistent ChromaDB — research chunks survive between runs
- JSON fence stripping and smart quote handling for gemma2:2b quirks

**Next:**

- Streamlit UI — frontend that calls the API and displays results
- Refinement loop — critic feeds back into research for better output
- Multi-tenant config — plug in any company's brand voice and categories
