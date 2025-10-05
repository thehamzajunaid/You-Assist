from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import os
from groq import Groq
import ollama
import uvicorn
from fastapi import APIRouter, Depends, Request
from models import ChatRequest, ChatResponse
from dotenv import load_dotenv
load_dotenv()
from services.document_store import DocumentStore, get_chroma_collection

groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))

chat_router = APIRouter(prefix="/api", tags=["Chat"])

@chat_router.post("/v1/chat", response_model=ChatResponse)
async def chat(data: ChatRequest, request: Request):
    """
    Main chat endpoint that processes user messages and returns AI responses
    """
    try:
        sources = None
        
        collection = get_chroma_collection(request)
        # If knowledge base is enabled and documents exist
        if data.use_knowledge_base and collection and collection.count() > 0:
            # Query ChromaDB for relevant chunks
            results = collection.query(
                query_texts=[data.message],
                n_results=min(3, collection.count()),
                include=["documents", "metadatas", "distances"]
            )
            
            if results and results['documents'] and results['documents'][0]:
                # Build context from search results
                documents = results['documents'][0]
                metadatas = results['metadatas'][0]
                distances = results['distances'][0]
                
                context_parts = []
                sources = []
                
                for doc, meta, dist in zip(documents, metadatas, distances):
                    context_parts.append(f"From {meta['filename']}:\n{doc}")
                    
                    # Convert distance to similarity score (lower distance = higher similarity)
                    similarity = 1 / (1 + dist)
                    
                    sources.append({
                        "filename": meta['filename'],
                        "chunk": doc[:200] + "..." if len(doc) > 200 else doc,
                        "score": round(similarity, 3)
                    })
                
                context = "\n\n".join(context_parts)
                
                # Augment the prompt with context
                augmented_message = f"""Based on the following context from uploaded documents, please answer the question.
                Context:
                {context}

                Question: {data.message}

                Please provide a comprehensive answer based on the context above. If the context doesn't contain enough information, please say so."""
                
            else:
                augmented_message = data.message + "\n\n(Note: No relevant information found in uploaded documents)"
        else:
            augmented_message = data.message
        
        # Prepare messages for Ollama
        messages = []
        
        # Add conversation history (limit to last 10 messages)
        recent_history = data.history[-10:] if len(data.history) > 10 else data.history
        for msg in recent_history:
            messages.append({
                "role": msg.role,
                "content": msg.content
            })

        # Prepare messages for Groq API
        messages = [
            {
                "role": "system",
                "content": "You are an assistant. Be specific and direct in your replies."
            }
        ]
        
        # Add conversation history
        for msg in data.history:
            messages.append({
                "role": msg.role,
                "content": msg.content
            })
        
        # Add current user message
        messages.append({
            "role": "user",
            "content": augmented_message
        })
        
        # Call Groq API
        chat_completion = groq_client.chat.completions.create(
            messages=messages,
            model="llama-3.1-8b-instant",
            temperature=0.7,
            max_tokens=1024,
            top_p=1,
            stream=False
        )

        #Call Ollama Local
        # chat_completion = ollama.chat(
        #     messages=messages,
        #     model="gemma3:1b",
        #     stream=False
        # )
        
        response_content = chat_completion.choices[0].message.content
        # response_content = chat_completion["message"]["content"]
        
        #Groq
        return ChatResponse(
            response=response_content,
            model=chat_completion.model,
            tokens_used=chat_completion.usage.total_tokens if hasattr(chat_completion, 'usage') else None,
            sources=sources if data.use_knowledge_base else None
        )

        #Ollama
        # return ChatResponse(
        #     response=response_content,
        #     model=chat_completion.get("model"),
        #     tokens_used=chat_completion.get("usage", {}).get("total_tokens"),
        #     sources=sources if data.use_knowledge_base else None
        # )

        
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=500,
            detail=f"Error processing chat request: {str(e)}"
        )