from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import os
import requests
import uvicorn
from PyPDF2 import PdfReader
from docx import Document
import io
from sentence_transformers import SentenceTransformer
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from fastapi import Request, HTTPException

# Initialize embedding model
embedding_model = SentenceTransformer('all-MiniLM-L6-v2')

# In-memory storage (resets on restart)
class DocumentStore:
    def __init__(self):
        self.documents = []  # List of {id, filename, content, chunks, embeddings}
        self.next_id = 1
    
    def add_document(self, filename: str, content: str):
        # Split content into chunks
        chunks = self._chunk_text(content, chunk_size=500, overlap=50)
        
        # Create embeddings
        embeddings = embedding_model.encode(chunks)
        
        doc = {
            "id": self.next_id,
            "filename": filename,
            "content": content,
            "chunks": chunks,
            "embeddings": embeddings
        }
        self.documents.append(doc)
        self.next_id += 1
        return doc["id"]
    
    def _chunk_text(self, text: str, chunk_size: int = 500, overlap: int = 50):
        """Split text into overlapping chunks"""
        words = text.split()
        chunks = []
        
        for i in range(0, len(words), chunk_size - overlap):
            chunk = ' '.join(words[i:i + chunk_size])
            if chunk:
                chunks.append(chunk)
        
        return chunks
    
    def search(self, query: str, top_k: int = 3):
        """Search for relevant chunks using semantic similarity"""
        if not self.documents:
            return []
        
        query_embedding = embedding_model.encode([query])[0]
        results = []
        
        for doc in self.documents:
            similarities = cosine_similarity([query_embedding], doc["embeddings"])[0]
            top_indices = np.argsort(similarities)[-top_k:][::-1]
            
            for idx in top_indices:
                if similarities[idx] > 0.3:  # Threshold for relevance
                    results.append({
                        "filename": doc["filename"],
                        "chunk": doc["chunks"][idx],
                        "score": float(similarities[idx])
                    })
        
        # Sort by score and return top results
        results.sort(key=lambda x: x["score"], reverse=True)
        return results[:top_k]
    
    def delete_document(self, doc_id: int):
        self.documents = [doc for doc in self.documents if doc["id"] != doc_id]
    
    def get_all_documents(self):
        return [{"id": doc["id"], "filename": doc["filename"], 
                 "chunks": len(doc["chunks"])} for doc in self.documents]
    
    def clear_all(self):
        self.documents = []
        self.next_id = 1


# services/document_service.py
from fastapi import Request, HTTPException

def get_chroma_collection(request: Request):
    collection = request.app.state.collection
    if collection is None:
        raise HTTPException(status_code=500, detail="ChromaDB not initialized")
    return collection

def chunk_text(text: str, chunk_size: int = 1000, overlap: int = 200) -> List[str]:
    """Split text into overlapping chunks"""
    chunks = []
    start = 0
    text_length = len(text)
    
    while start < text_length:
        end = start + chunk_size
        chunk = text[start:end]
        
        # Try to break at sentence boundary
        if end < text_length:
            last_period = chunk.rfind('.')
            last_newline = chunk.rfind('\n')
            break_point = max(last_period, last_newline)
            
            if break_point > chunk_size * 0.5:
                chunk = chunk[:break_point + 1]
                end = start + break_point + 1
        
        if chunk.strip():
            chunks.append(chunk.strip())
        
        start = end - overlap
    
    return chunks