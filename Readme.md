# 📄🧠 RAG Chat Assistant with Pinecone + LLaMA

A Retrieval-Augmented Generation (RAG) chatbot that allows users to upload PDF documents and interactively ask questions about their content. Built with a **modular architecture** using LangChain, Pinecone, Ollama (LLaMA), and Streamlit.

---

## 🚀 Features

- **PDF Upload & Parsing** — Upload any PDF and extract its text for analysis
- **Semantic Search** — Uses Pinecone vector database with HuggingFace embeddings
- **PDF Isolation** — Each PDF stored in its own Pinecone namespace; queries never cross-contaminate
- **Metadata Tracking** — Stores pdf_id, name, upload date, chunk info per vector
- **Custom Prompt Template** — Structured prompts for accurate, factual answers
- **Source Transparency** — Shows which chunks were used to generate the answer
- **Chat History** — Tracks Q&A pairs per session
- **Modular Codebase** — Clean separation of concerns across multiple modules

---

## 📁 Project Structure

```
rag_modular_project/
│
├── app_modular.py              # Main Streamlit entry point & orchestrator
├── config.py                   # All configurations & environment variables
├── requirements.txt            # Python dependencies
├── .env                        # Secret keys (NOT committed to git)
├── .env.example                # Template for .env file
├── .gitignore                  # Ignores .env, venv, __pycache__, etc.
│
├── utils/                      # Data processing utilities
│   ├── __init__.py
│   ├── pdf_processor.py        # PDF text extraction & chunking
│   ├── embeddings.py           # Embedding model initialization
│   └── prompts.py              # Prompt templates for LLM
│
├── database/                   # Vector database layer
│   ├── __init__.py
│   ├── pinecone_manager.py     # Pinecone client & index management
│   └── vector_store.py         # Store & search vectors with metadata
│
├── retrieval/                  # Retrieval & QA logic
│   ├── __init__.py
│   ├── retriever.py            # Document retrieval configuration
│   └── qa_chain.py             # QA chain using LCEL pipeline
│
└── frontend/                   # Streamlit UI layer
    ├── __init__.py
    ├── ui_components.py        # Reusable display components
    └── session_manager.py      # Session state management
```

---

## 🛠️ Technologies Used

| Technology | Purpose | Version |
|-----------|---------|---------|
| **Python** | Core language | 3.10+ |
| **Streamlit** | Web UI | Latest |
| **LangChain** | RAG pipeline orchestration | Latest |
| **langchain-core** | LCEL chain building | Latest |
| **langchain-community** | Ollama LLM integration | Latest |
| **langchain-pinecone** | Pinecone vector store | Latest |
| **langchain-text-splitters** | Text chunking | Latest |
| **langchain-huggingface** | HuggingFace embeddings | Latest |
| **Pinecone** | Cloud vector database | Latest |
| **HuggingFace** | Sentence embeddings | BAAI/bge-large-en-v1.5 |
| **Ollama** | Local LLM runner | Latest |
| **LLaMA 3** | Language model for QA | llama3:instruct |
| **PyPDF2** | PDF text extraction | Latest |
| **python-dotenv** | .env file loading | Latest |

---

## 🏗️ Architecture

### System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    STREAMLIT WEB UI                          │
│               (frontend/ui_components.py)                    │
└──────────────────────┬──────────────────────────────────────┘
                       │
          ┌────────────┴────────────┐
          │                         │
          ▼                         ▼
  ┌──────────────┐         ┌────────────────┐
  │  PDF Upload  │         │ Question Input │
  └──────┬───────┘         └───────┬────────┘
         │                         │
         ▼                         │
  ┌──────────────────┐             │
  │  PyPDF2 Parser   │             │
  │  (extract text)  │             │
  └──────┬───────────┘             │
         │                         │
         ▼                         │
  ┌──────────────────┐             │
  │  Text Chunking   │             │
  │  chunk_size=1000 │             │
  │  overlap=200     │             │
  └──────┬───────────┘             │
         │                         │
         ▼                         │
  ┌──────────────────┐             │
  │  BAAI/bge-large  │             │
  │  Embeddings      │             │
  │  (1024 dims)     │             │
  └──────┬───────────┘             │
         │                         │
         ▼                         │
  ┌──────────────────────────────┐ │
  │       PINECONE               │ │
  │  Index: chat-assistant       │ │
  │  Namespace: <pdf_id>         │ │
  │  Metric: cosine              │ │
  │  Metadata: pdf_id, name,     │ │
  │  chunk_index, upload_date    │ │
  └──────┬───────────────────────┘ │
         │                         │
         └──────────┬──────────────┘
                    │
                    ▼
          ┌─────────────────┐
          │ Embed Query     │
          │ Search Pinecone │
          │ Filter: pdf_id  │
          │ Top K=5 chunks  │
          └────────┬────────┘
                   │
                   ▼
          ┌─────────────────┐
          │ Prompt Template │
          │ + Context       │
          │ + Question      │
          └────────┬────────┘
                   │
                   ▼
          ┌─────────────────┐
          │ LLaMA 3 Instruct│
          │ (via Ollama)    │
          │ temp=0.2        │
          └────────┬────────┘
                   │
                   ▼
          ┌─────────────────┐
          │ Answer + Source │
          │ Documents       │
          └─────────────────┘
```

### Data Flow

**Upload Flow:**
```
PDF → Extract Text → Chunk (1000 chars) → Embed (1024 dims) → Pinecone (with metadata)
```

**Query Flow:**
```
Question → Embed → Search Pinecone (filter by pdf_id) → Top 5 Chunks → Prompt → LLaMA → Answer
```

---

## ⚡ Getting Started

### Prerequisites

- Python 3.10+
- [Ollama](https://ollama.com/download) installed
- [Pinecone](https://www.pinecone.io) account (free tier works)

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/rag-chatbot.git
cd rag-chatbot
```

### 2. Create Virtual Environment

```bash
python -m venv venv

# Activate on Windows
venv\Scripts\activate

# Activate on Mac/Linux
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Setup .env File

Create a `.env` file in the project root:

```env
PINECONE_API_KEY=your-pinecone-api-key-here
PINECONE_ENVIRONMENT=us-east-1
```

Get your API key from [pinecone.io](https://www.pinecone.io) → API Keys section.

### 5. Setup Ollama

```bash
# Install Ollama from https://ollama.com/download

# Pull the required model
ollama pull llama3:instruct

# Start Ollama server (keep this running!)
ollama serve
```

### 6. Run the App

Open a **new terminal** (keep Ollama running in the first one):

```bash
streamlit run app_modular.py
```

Visit [http://localhost:8501](http://localhost:8501)

---

## 📦 Requirements

```txt
streamlit
PyPDF2
python-dotenv
langchain
langchain-community
langchain-pinecone
langchain-core
langchain-text-splitters
langchain-huggingface
pinecone
sentence-transformers
langsmith
```

---

## ⚙️ Configuration (config.py)

All settings are centralized in `config.py`:

```python
# Pinecone
INDEX_NAME = "chat-assistant"
PINECONE_CLOUD = "aws"
PINECONE_ENVIRONMENT = "us-east-1"

# Embeddings
EMBEDDING_MODEL_NAME = "BAAI/bge-large-en-v1.5"
EMBEDDING_DIMENSION = 1024

# Chunking
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200

# Retrieval
TOP_K_RESULTS = 5
SIMILARITY_METRIC = "cosine"

# LLM
LLM_MODEL = "llama3:instruct"
LLM_TEMPERATURE = 0.2
```

---

## 📝 Example Usage

1. **Start Ollama:** `ollama serve`
2. **Run App:** `streamlit run app_modular.py`
3. **Upload PDF** using the file uploader
4. **Wait** for processing (embedding + Pinecone storage)
5. **Ask questions** like:
   - *"What is the main topic of this document?"*
   - *"Summarize the key findings"*
   - *"What does the document say about X?"*
6. **View source chunks** to verify the answer

---

## 🔧 Common Errors & Fixes

| Error | Fix |
|-------|-----|
| `ModuleNotFoundError: langchain.chains` | Use LCEL pipeline in qa_chain.py |
| `ModuleNotFoundError: langchain.text_splitter` | `from langchain_text_splitters import ...` |
| `ModuleNotFoundError: langchain.prompts` | `from langchain_core.prompts import ...` |
| `ModuleNotFoundError: langchain.schema` | `from langchain_core.retrievers import ...` |
| `pinecone-client` renamed error | Use `pinecone` package instead |
| `Vector dimension mismatch` | Delete index, recreate with correct dimension |
| `Ollama connection refused` | Run `ollama serve` in a separate terminal |
| `get_relevant_documents` error | Replace with `.invoke(query)` |

---

## 🏆 Design Qualities

### ✅ Scalability
- Pinecone handles millions of vectors with auto-scaling
- Serverless architecture — no capacity planning needed
- Namespace isolation supports unlimited PDFs

### ✅ Modularity
- Each module has a single, well-defined responsibility
- Easy to swap components (e.g., different LLM or vector DB)
- Clean imports via `__init__.py` files

### ✅ Data Isolation
- Each PDF stored in its own Pinecone namespace
- Metadata filter ensures queries only retrieve from selected PDF
- No cross-document contamination

### ✅ Maintainability
- Centralized config — change settings in one place
- Well-documented functions with docstrings
- Clear data flow through the pipeline

### ✅ Transparency
- Source chunks displayed with every answer
- Metadata shows chunk index, upload date, PDF name
- Easy to verify and fact-check answers

---

## 🔄 Extending the Project

### Swap the LLM
In `config.py`:
```python
LLM_MODEL = "mistral"  # or "gemma", "phi3", etc.
```

### Change Embedding Model
In `config.py`:
```python
EMBEDDING_MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
EMBEDDING_DIMENSION = 384
```
> ⚠️ Delete and recreate Pinecone index if changing embedding model!

### Adjust Chunking
In `config.py`:
```python
CHUNK_SIZE = 500      # Smaller chunks = more precise
CHUNK_OVERLAP = 100
```

### Retrieve More Context
In `config.py`:
```python
TOP_K_RESULTS = 10   # Retrieve more chunks per query
```

---

## 🙏 Acknowledgements

- [LangChain](https://github.com/hwchase17/langchain) — RAG pipeline framework
- [Pinecone](https://www.pinecone.io) — Cloud vector database
- [Ollama](https://ollama.com) — Local LLM runner
- [BAAI/bge-large-en-v1.5](https://huggingface.co/BAAI/bge-large-en-v1.5) — Embedding model
- [Streamlit](https://streamlit.io) — Web UI framework

---

## 📄 License

This project is licensed under the MIT License.
