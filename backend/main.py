from typing import Union

from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from api.v1 import chat, index
from routes import user_router
from services.document_store import DocumentStore
import chromadb
from chromadb.config import Settings
import uuid
import atexit
import shutil
import io
import os

app = FastAPI()

# CORS middleware to allow frontend requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:3001"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize ChromaDB client (in-memory with persistence for session)
CHROMA_PATH = "./chroma_db"
chroma_client = chromadb.Client(Settings(
    persist_directory=CHROMA_PATH,
    anonymized_telemetry=False
))

# Get or create collection
try:
    collection = chroma_client.get_or_create_collection(
        name="documents",
        metadata={"hnsw:space": "cosine"}
    )
    print(f"✅ ChromaDB initialized. Collection has {collection.count()} documents.")
except Exception as e:
    print(f"⚠️ Error initializing ChromaDB: {e}")
    collection = None

app.state.chroma_client = chroma_client
app.state.collection = collection
app.state.document_metadata = {}


def cleanup_chroma():
    """Cleanup ChromaDB on app shutdown"""
    try:
        if os.path.exists(CHROMA_PATH):
            shutil.rmtree(CHROMA_PATH)
            print("✅ ChromaDB cleaned up successfully")
    except Exception as e:
        print(f"⚠️ Error cleaning up ChromaDB: {e}")

# Register cleanup on exit
atexit.register(cleanup_chroma)

@app.on_event("startup")
async def startup_event():
    """Initialize vector store on startup"""
    print("🚀 Starting AI Assistant API with ChromaDB...")
    print(f"📊 Vector store location: {CHROMA_PATH}")
    if collection:
        print(f"📚 Current documents in collection: {collection.count()}")

@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown"""
    print("🛑 Shutting down AI Assistant API...")
    cleanup_chroma()

app.include_router(user_router.router)
app.include_router(chat.chat_router)
app.include_router(index.router)

@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "message": "AI Assistant API is running",
        "version": "1.0.0"
    }