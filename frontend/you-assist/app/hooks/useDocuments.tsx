// hooks/useDocuments.ts
"use client";
import { useState, useEffect } from 'react';

interface Document {
  id: string;
  filename: string;
  chunks: number;
}

export function useDocuments() {
  const [documents, setDocuments] = useState<Document[]>([]);
  const [uploading, setUploading] = useState(false);
  const [useKnowledgeBase, setUseKnowledgeBase] = useState(false);

  const fetchDocuments = async () => {
    try {
      const response = await fetch(`${process.env.NEXT_PUBLIC_API_SERVER}/api/v1/documents`);
      if (response.ok) {
        const data = await response.json();
        setDocuments(data);
      }
    } catch (err) {
      console.error('Error fetching documents:', err);
    }
  };

  useEffect(() => {
    fetchDocuments();
  }, []);

  const uploadDocument = async (file: File): Promise<string | null> => {
    const formData = new FormData();
    formData.append('file', file);

    setUploading(true);
    try {
      const response = await fetch(`${process.env.NEXT_PUBLIC_API_SERVER}/api/v1/index`, {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        const error = await response.json();
        throw new Error(error.detail || 'Upload failed');
      }

      const data = await response.json();
      await fetchDocuments();
      
      return `✅ Document "${data.filename}" uploaded successfully! Created ${data.chunks_created} knowledge chunks. You can now toggle "Knowledge Base" mode to ask questions about this document.`;
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Unknown error';
      return `❌ Error uploading document: ${errorMessage}`;
    } finally {
      setUploading(false);
    }
  };

  const deleteDocument = async (docId: string): Promise<string | null> => {
    try {
      const response = await fetch(`${process.env.NEXT_PUBLIC_API_SERVER}/api/v1/documents/${docId}`, {
        method: 'DELETE',
      });

      if (response.ok) {
        await fetchDocuments();
        return '🗑️ Document deleted from knowledge base.';
      }
      return null;
    } catch (err) {
      console.error('Error deleting document:', err);
      return null;
    }
  };

  const deleteAllDocuments = async (): Promise<string | null> => {
    if (!window.confirm('Delete all documents from knowledge base?')) {
      return null;
    }
    
    try {
      const response = await fetch(`${process.env.NEXT_PUBLIC_API_SERVER}/api/v1/documents`, {
        method: 'DELETE',
      });

      if (response.ok) {
        setDocuments([]);
        setUseKnowledgeBase(false);
        return '🗑️ All documents cleared from knowledge base.';
      }
      return null;
    } catch (err) {
      console.error('Error deleting documents:', err);
      return null;
    }
  };

  return {
    documents,
    uploading,
    useKnowledgeBase,
    setUseKnowledgeBase,
    uploadDocument,
    deleteDocument,
    deleteAllDocuments,
  };
}