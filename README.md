# TechRivo RAG Chatbot

**AI-Powered Knowledge Base Assistant with Retrieval-Augmented Generation**



##  Features

### Core Capabilities
-**Retrieval-Augmented Generation (RAG)** - Combines vector search with LLM generation for accurate, grounded responses
**Multi-Format Document Ingestion** - Supports PDF, DOCX, TXT, CSV file formats
**Semantic Search** - ChromaDB vector database with OpenAI embeddings for intelligent context retrieval
**Real-Time Streaming** - Server-Sent Events (SSE) for live response streaming
**Persistent Knowledge Base** - Data persists across restarts with ChromaDB storage
**Web Scraping** - Automated website content extraction and processing
**Context-Aware Responses** - Maintains conversation history for coherent multi-turn dialogues

### Technical Features
**Docker Support** - Fully containerized with docker-compose orchestration
**CORS Configuration** - Secure cross-origin resource sharing
**Health Checks** - Built-in API health monitoring endpoints
**Relevance Scoring** - Document ranking based on similarity scores
**Async Operations** - Non-blocking architecture for high performance
**Type Safety** - Full Python type hints and Pydantic models

### User Experience
**Modern UI** - Clean, responsive React interface with TechRivo branding
**Real-Time Indicators** - Connection status and typing animations
**Mobile Responsive** - Works seamlessly across all devices
**Error Handling** - Graceful error messages and fallback responses

---

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                        User Browser                          │
│                     (React Frontend)                         │
└─────────────────────┬───────────────────────────────────────┘
                      │ HTTP/SSE
                      ▼
┌─────────────────────────────────────────────────────────────┐
│                    Nginx Reverse Proxy                       │
│              (Routing, Static Files, CORS)                   │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│                   FastAPI Backend                            │
│                                                              │
│  ┌────────────┐  ┌──────────────┐  ┌──────────────┐       │
│  │   Routes   │  │  RAG Agent   │  │   LLM        │       │
│  │  (API)     │→ │  (Orchestr.) │→ │   Service    │       │
│  └────────────┘  └──────────────┘  └──────────────┘       │
│                         │                    │               │
│                         ▼                    ▼               │
│                  ┌──────────────┐    ┌──────────────┐      │
│                  │  Retriever   │    │   OpenAI     │      │
│                  │              │    │   API        │      │
│                  └──────────────┘    └──────────────┘      │
│                         │                                    │
│                         ▼                                    │
│                  ┌──────────────┐                           │
│                  │  Embeddings  │                           │
│                  │   Service    │                           │
│                  └──────────────┘                           │
│                         │                                    │
│                         ▼                                    │
│                  ┌──────────────┐                           │
│                  │  Vector DB   │                           │
│                  │  (ChromaDB)  │                           │
│                  └──────────────┘                           │
└─────────────────────────────────────────────────────────────┘
```

### Data Flow

1. **User Query** → React frontend captures user input
2. **API Request** → Sends POST request to `/api/chat/stream`
3. **Query Embedding** → Backend converts query to vector using OpenAI embeddings
4. **Vector Search** → ChromaDB retrieves top-k similar documents
5. **Context Preparation** → Retriever formats documents into context string
6. **LLM Generation** → OpenAI GPT-4 generates response with context
7. **Streaming Response** → SSE streams tokens back to frontend in real-time
8. **UI Update** → React displays streaming response character-by-character



### Environment Variable Reference

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `OPENAI_API_KEY` |  Yes | - | OpenAI API key for embeddings and generation |
| `CHROMA_PERSIST_DIRECTORY` | No | `./backend/chroma_db` | ChromaDB data storage location |
| `ENVIRONMENT` | No | `development` | Application environment |
| `LLM_MODEL` | No | `gpt-4-turbo-preview` | OpenAI model for generation |
| `LLM_TEMPERATURE` | No | `0.7` | Response randomness (0.0-1.0) |
| `MAX_TOKENS` | No | `2000` | Maximum tokens in response |
| `RETRIEVAL_TOP_K` | No | `5` | Number of documents to retrieve |

---

## Project Structure

```
techrivo-rag-chatbot/
├── backend/                      # Python FastAPI backend
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py              # Application entry point
│   │   ├── config.py            # Configuration management
│   │   ├── routes/              # API endpoints
│   │   │   ├── chat.py          # Chat endpoints
│   │   │   ├── health.py        # Health check
│   │   │   └── ingest.py        # Document ingestion
│   │   ├── rag/                 # RAG pipeline components
│   │   │   ├── embeddings.py    # Embedding service
│   │   │   ├── vector_store.py  # ChromaDB interface
│   │   │   ├── retriever.py     # Document retrieval
│   │   │   ├── llm_service.py   # OpenAI integration
│   │   │   └── rag_agent.py     # Main orchestrator
│   │   └── ingestion/           # Document processing
│   │       ├── loaders.py       # File loaders
│   │       ├── processor.py     # Text processing
│   │       └── web_scraper.py   # Web scraping
│   ├── chroma_db/               # Vector database storage
│   ├── docs/                    # Document uploads
│   ├── requirements.txt         # Python dependencies
│   ├── .env                     # Environment variables
│   ├── .dockerignore
│   ├── ingest_techrivo.py       # TechRivo data ingestion
│   └── ingest_docs.py           # Document ingestion script
│
├── frontend/                    # React frontend (or at root)
│   ├── src/
│   │   ├── App.jsx              # Main component
│   │   ├── main.jsx             # Entry point
│   │   └── index.css            # Global styles
│   ├── public/                  # Static assets
│   ├── package.json             # Node dependencies
│   ├── vite.config.js           # Vite configuration
│   └── .dockerignore
│
├── Dockerfile.backend           # Backend container
├── Dockerfile.frontend          # Frontend container
├── docker-compose.yml           # Multi-container orchestration
├── nginx.conf                   # Nginx configuration
├── .env                         # Root environment variables
├── .env.example                 # Environment template
├── .gitignore                   # Git ignore rules
└── README.md                    # This file
```

---

