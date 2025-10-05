from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import os
from groq import Groq
import ollama
import uvicorn
from fastapi import APIRouter
from models import ChatRequest, ChatResponse
from dotenv import load_dotenv
load_dotenv()

groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))

chat_router = APIRouter(prefix="/api", tags=["Chat"])

@chat_router.post("/v1/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    Main chat endpoint that processes user messages and returns AI responses
    """
    try:
        # Prepare messages for Groq API
        messages = [
            {
                "role": "system",
                "content": "You are an assistant. Be specific and direct in your replies."
            }
        ]
        
        # Add conversation history
        for msg in request.history:
            messages.append({
                "role": msg.role,
                "content": msg.content
            })
        
        # Add current user message
        messages.append({
            "role": "user",
            "content": request.message
        })
        
        # Call Groq API
        # chat_completion = groq_client.chat.completions.create(
        #     messages=messages,
        #     model="llama-3.1-8b-instant",
        #     temperature=0.7,
        #     max_tokens=1024,
        #     top_p=1,
        #     stream=False
        # )

        #Call Ollama Local
        chat_completion = ollama.chat(
            messages=messages,
            model="gemma3:1b",
            stream=False
        )
        
        response_content = chat_completion.message.content
        
        return ChatResponse(
            response=response_content,
            model=chat_completion.model,
            tokens_used=chat_completion.usage.total_tokens if hasattr(chat_completion, 'usage') else None
        )
        
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=500,
            detail=f"Error processing chat request: {str(e)}"
        )