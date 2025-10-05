# 🤖 AI Assistant with RAG - Democratizing AI Through Open Source

> A Retrieval Augmented Generation (RAG) system built with modern tech stack, demonstrating practical AI implementation accessible to everyone.

[![Next.js](https://img.shields.io/badge/Next.js-14-black)](https://nextjs.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104-009688)](https://fastapi.tiangolo.com/)
[![ChromaDB](https://img.shields.io/badge/ChromaDB-Vector_DB-orange)](https://www.trychroma.com/)
[![Ollama](https://img.shields.io/badge/Ollama-Local_LLM-blue)](https://ollama.ai/)

## 🎯 Project Vision

**Democratizing AI** means making advanced AI technologies accessible without expensive APIs or cloud dependencies. This project demonstrates how anyone can build production-grade AI applications using **100% free, open-source tools** that run entirely on local hardware.

## ✨ Key Features

- **🔍 Semantic Search**: ChromaDB vector database for intelligent document retrieval
- **📚 Document Q&A**: Upload PDFs, DOCX, TXT files and query their contents
- **🤖 Local LLM**: Ollama integration - no API costs, complete data privacy
- **⚡ Real-time RAG**: Context-aware responses with source citations
- **🎨 Modern UI**: Clean, responsive interface built with Next.js and Tailwind CSS
- **🔄 Session-based**: In-memory vector store with automatic cleanup

## 🏗️ Architecture

```
┌─────────────┐      ┌──────────────┐      ┌─────────────┐
│   Next.js   │ ───→ │   FastAPI    │ ───→ │  ChromaDB   │
│  Frontend   │      │   Backend    │      │ Vector Store│
└─────────────┘      └──────────────┘      └─────────────┘
                            │
                            ↓
                     ┌──────────────┐
                     │    Ollama    │
                     │   Local LLM  │
                     └──────────────┘
```

**Tech Stack:**
- **Frontend**: Next.js 14, TypeScript, Tailwind CSS
- **Backend**: FastAPI, Python 3.10
- **Vector DB**: ChromaDB with automatic embeddings
- **LLM**: Ollama (gemma3:1b, mistral, or any supported model)

## 🚀 Quick Start

### Prerequisites

- Node.js 18+
- Python 3.9+
- Ollama installed ([Download here](https://ollama.ai/))

### 1. Clone Repository

```bash
git clone https://github.com/thehamzajunaid/you-assist.git
cd you-assist
```

### 2. Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Start backend
python main.py
```

Backend runs on `http://localhost:8000`

### 3. Frontend Setup

```bash
cd frontend
cd you-assist

# Install dependencies
npm install

# Start development server
npm run dev
```

Frontend runs on `http://localhost:3000`

### 4. Ollama Setup

```bash
# Install Ollama (if not already installed)
# Visit: https://ollama.ai/download

# Pull a model
ollama pull gemma3:1b

# Start Ollama server
ollama serve
```

Ollama runs on `http://localhost:11434`

### 5. Optional: Environment Variables

```bash
# backend/.env (optional)
GROQ_API_KEY=YOUR-GROQ-API-KEY (Only needed if you are opting for non local inference. Uncomment the GROQ code for chatting in backend/api/v1/chat.py)

# frontend/you-assist/.env.local
NEXT_PUBLIC_API_SERVER=http://localhost:8000
```

## 📖 Usage

1. **Upload Documents**: Click "Upload Document" and select PDF, DOCX, or TXT files
2. **Enable Knowledge Base**: Toggle "Use Knowledge Base" mode
3. **Ask Questions**: Query your documents - get AI-powered answers with source citations
4. **Manage Documents**: Delete individual documents or clear all

## 🎓 Technical Highlights

### RAG Implementation
- **Text Chunking**: Intelligent splitting with overlap for context preservation
- **Vector Embeddings**: Automatic semantic embeddings via ChromaDB
- **Semantic Search**: Cosine similarity for relevant chunk retrieval
- **Context Augmentation**: LLM prompts enriched with retrieved documents

### Production-Ready Features
- **Async Processing**: Non-blocking I/O for better performance
- **Error Handling**: Comprehensive error management and user feedback
- **Type Safety**: Full TypeScript support on frontend
- **API Documentation**: Auto-generated OpenAPI docs at `/docs`
- **Lifecycle Management**: Automatic vector store cleanup on shutdown

## 🔬 Research & Learning Outcomes

This project demonstrates:

1. **Practical RAG Architecture**: Industry-standard approach to building AI applications
2. **Vector Database Integration**: Understanding of embeddings and semantic search
3. **LLM Integration**: Working with both local and API-based language models
4. **Full-Stack AI Development**: End-to-end implementation from UI to vector store
5. **Cloud-Ready Design**: Microservices architecture suitable for containerization

## 🌟 Why This Matters

**Accessibility**: No API costs, runs on consumer hardware
**Privacy**: All data stays local, no external API calls
**Scalability**: Architecture ready for production deployment
**Education**: Clear, documented code for learning and extension

## 🛣️ Roadmap

- [ ] Multi-modal support (images, videos)
- [ ] Conversation persistence with database
- [ ] User authentication and multi-tenancy
- [ ] Streaming responses for real-time feedback
- [ ] Hybrid search (keyword + semantic)
- [ ] Docker containerization
- [ ] Cloud deployment guides (Azure, AWS, GCP)

## 📚 Resources

- [ChromaDB Documentation](https://docs.trychroma.com/)
- [Ollama Models](https://ollama.ai/library)
- [FastAPI Guide](https://fastapi.tiangolo.com/)
- [RAG Best Practices](https://www.pinecone.io/learn/retrieval-augmented-generation/)

## 🤝 Contributing

Contributions welcome! This project aims to make AI accessible to everyone.

## 📄 License

MIT License - Free to use, modify, and distribute

---

**Built with the mission of democratizing AI through open-source technology** 🚀

*For questions or collaboration: [Your Contact Info]*