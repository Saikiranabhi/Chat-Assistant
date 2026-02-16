# Modular RAG Application Architecture

## Project Structure

```
rag-chatbot/
│
├── app.py                      # Main Streamlit frontend
├── config.py                   # Configuration & environment variables
├── requirements.txt            # Dependencies
│
├── utils/
│   ├── __init__.py
│   ├── pdf_processor.py        # PDF text extraction & preprocessing
│   ├── embeddings.py           # Embedding generation utilities
│   └── prompts.py              # Prompt templates
│
├── database/
│   ├── __init__.py
│   ├── pinecone_manager.py     # Pinecone initialization & management
│   └── vector_store.py         # Vector storage operations
│
├── retrieval/
│   ├── __init__.py
│   ├── retriever.py            # Retrieval logic
│   └── qa_chain.py             # QA chain construction
│
└── frontend/
    ├── __init__.py
    ├── ui_components.py        # Reusable UI components
    └── session_manager.py      # Session state management
```

## Component Responsibilities

### 1. **config.py**
- Environment variables
- Model configurations
- Pinecone settings
- Constants

### 2. **utils/pdf_processor.py**
- PDF text extraction
- Text cleaning
- Chunking logic

### 3. **utils/embeddings.py**
- Embedding model initialization
- Text-to-vector conversion
- Batch processing

### 4. **utils/prompts.py**
- Prompt templates
- Prompt formatting
- Instructions

### 5. **database/pinecone_manager.py**
- Pinecone client initialization
- Index creation/management
- Connection handling

### 6. **database/vector_store.py**
- Store embeddings with metadata
- Search operations
- Namespace management

### 7. **retrieval/retriever.py**
- Query processing
- Similarity search
- Result filtering

### 8. **retrieval/qa_chain.py**
- LLM initialization
- QA chain construction
- Response generation

### 9. **frontend/ui_components.py**
- File uploader
- Question input
- Answer display
- Source viewer

### 10. **frontend/session_manager.py**
- Session state handling
- PDF tracking
- Cache management

### 11. **app.py**
- Main orchestration
- Route handling
- Component integration

## Data Flow

```
User Upload (app.py)
    ↓
PDF Processing (utils/pdf_processor.py)
    ↓
Embedding Generation (utils/embeddings.py)
    ↓
Vector Storage (database/vector_store.py)
    ↓
Pinecone (database/pinecone_manager.py)

User Query (app.py)
    ↓
Retrieval (retrieval/retriever.py)
    ↓
QA Chain (retrieval/qa_chain.py)
    ↓
Display (frontend/ui_components.py)
```

## Benefits of Modular Design

✅ **Separation of Concerns** - Each module has single responsibility
✅ **Reusability** - Components can be imported elsewhere
✅ **Testability** - Easy to unit test each module
✅ **Maintainability** - Changes isolated to specific files
✅ **Scalability** - Can swap implementations easily
✅ **Collaboration** - Multiple developers can work simultaneously