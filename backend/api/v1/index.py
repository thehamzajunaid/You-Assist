from fastapi import APIRouter, Depends, Request
from fastapi import FastAPI, HTTPException, UploadFile, File
from services.retriever import extract_text_from_docx, extract_text_from_pdf, extract_text_from_txt
from services.document_store import get_chroma_collection, chunk_text
import uuid
from models import DocumentInfo
from typing import List


router = APIRouter(prefix="/api", tags=["Index"])
@router.post("/v1/index")
async def upload_document(request: Request, file: UploadFile = File(...)):
    """
    Upload and process a document into ChromaDB
    """
    collection = get_chroma_collection(request)
    if not collection:
        raise HTTPException(status_code=503, detail="Vector database not initialized")
    
    try:
        # Check file size (limit to 10MB)
        content = await file.read()
        if len(content) > 10 * 1024 * 1024:
            raise HTTPException(
                status_code=400,
                detail="File too large. Maximum size is 10MB."
            )
        
        filename = file.filename.lower()
        
        # Extract text based on file type
        if filename.endswith('.pdf'):
            text = extract_text_from_pdf(content)
        elif filename.endswith('.docx'):
            text = extract_text_from_docx(content)
        elif filename.endswith('.txt'):
            text = extract_text_from_txt(content)
        else:
            raise HTTPException(
                status_code=400,
                detail="Unsupported file type. Please upload PDF, DOCX, or TXT files."
            )
        
        if not text.strip():
            raise HTTPException(
                status_code=400,
                detail="No text could be extracted from the document."
            )
        
        # Create chunks
        chunks = chunk_text(text, chunk_size=1000, overlap=200)
        
        # Generate document ID
        doc_id = str(uuid.uuid4())
        
        # Prepare data for ChromaDB
        chunk_ids = [f"{doc_id}_chunk_{i}" for i in range(len(chunks))]
        metadatas = [
            {
                "document_id": doc_id,
                "filename": file.filename,
                "chunk_index": i,
                "total_chunks": len(chunks)
            }
            for i in range(len(chunks))
        ]
        
        # Add to ChromaDB (it will automatically generate embeddings)
        collection.add(
            documents=chunks,
            metadatas=metadatas,
            ids=chunk_ids
        )
        
        # Store document metadata
        request.app.state.document_metadata[doc_id] = {
            "filename": file.filename,
            "chunks": len(chunks),
            "chunk_ids": chunk_ids
        }
        
        print(f"✅ Added document '{file.filename}' with {len(chunks)} chunks to vector DB")
        
        return {
            "message": "Document uploaded successfully",
            "document_id": doc_id,
            "filename": file.filename,
            "chunks_created": len(chunks)
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error processing document: {str(e)}"
        )

@router.get("/v1/documents", response_model=List[DocumentInfo])
async def get_documents(request: Request):
    """
    Get list of all uploaded documents
    """
    return [
        DocumentInfo(
            id=uuid.UUID(str(doc_id)),
            filename=meta["filename"],
            chunks=meta["chunks"]
        )
        for doc_id, meta in request.app.state.document_metadata.items()
    ]


@router.delete("/v1/documents/{doc_id}")
async def delete_document(doc_id: str, request: Request):
    """
    Delete a specific document from the vector database
    """
    collection = get_chroma_collection(request)
    document_metadata = request.app.state.document_metadata
    if not collection:
        raise HTTPException(status_code=503, detail="Vector database not initialized")
    
    if doc_id not in document_metadata:
        raise HTTPException(status_code=404, detail="Document not found")
    
    try:
        # Get chunk IDs for this document
        chunk_ids = document_metadata[doc_id]["chunk_ids"]
        
        # Delete from ChromaDB
        collection.delete(ids=chunk_ids)
        
        # Remove from metadata
        filename = document_metadata[doc_id]["filename"]
        del document_metadata[doc_id]
        
        print(f"🗑️ Deleted document '{filename}' from vector DB")
        
        return {"message": "Document deleted successfully"}
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error deleting document: {str(e)}"
        )
    
@router.delete("/v1/documents")
async def delete_all_documents(request: Request):
    """
    Delete all documents from the vector database
    """
    collection = get_chroma_collection(request)
    document_metadata = request.app.state.document_metadata
    if not collection:
        raise HTTPException(status_code=503, detail="Vector database not initialized")
    
    try:
        # Get all chunk IDs
        all_chunk_ids = []
        for meta in document_metadata.values():
            all_chunk_ids.extend(meta["chunk_ids"])
        
        if all_chunk_ids:
            # Delete from ChromaDB
            collection.delete(ids=all_chunk_ids)
        
        # Clear metadata
        document_metadata.clear()
        
        print("🗑️ Deleted all documents from vector DB")
        
        return {"message": "All documents deleted successfully"}
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error deleting documents: {str(e)}"
        )