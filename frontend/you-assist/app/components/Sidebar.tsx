// components/Sidebar.tsx
"use client";
import { useState, useRef } from 'react';
import { Upload, Sparkles, File, X, BookOpen, Trash2, Loader2 } from 'lucide-react';

interface Document {
  id: string;
  filename: string;
  chunks: number;
}

interface SidebarProps {
  documents: Document[];
  useKnowledgeBase: boolean;
  setUseKnowledgeBase: (value: boolean) => void;
  onUpload: (file: File) => Promise<void>;
  onDeleteDocument: (id: string) => Promise<void>;
  onDeleteAll: () => Promise<void>;
  uploading: boolean;
}

export default function Sidebar({
  documents,
  useKnowledgeBase,
  setUseKnowledgeBase,
  onUpload,
  onDeleteDocument,
  onDeleteAll,
  uploading
}: SidebarProps) {
  const fileInputRef = useRef<HTMLInputElement>(null);

  const handleFileChange = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) {
      await onUpload(file);
      if (fileInputRef.current) {
        fileInputRef.current.value = '';
      }
    }
  };

  return (
    <div className="w-80 bg-white/10 backdrop-blur-lg rounded-2xl shadow-2xl border border-white/20 p-6 flex flex-col gap-4">
      {/* Header */}
      <div className="flex items-center gap-3 pb-4 border-b border-white/20">
        <Sparkles className="w-6 h-6 text-purple-400" />
        <h2 className="text-xl font-bold text-white">Knowledge Base</h2>
      </div>

      {/* Upload Section */}
      <div className="space-y-3">
        <input
          ref={fileInputRef}
          type="file"
          accept=".pdf,.docx,.txt"
          onChange={handleFileChange}
          className="hidden"
        />
        <button
          onClick={() => fileInputRef.current?.click()}
          disabled={uploading}
          className="w-full bg-gradient-to-r from-purple-600 to-blue-600 text-white py-3 rounded-xl hover:from-purple-700 hover:to-blue-700 transition-all disabled:opacity-50 flex items-center justify-center gap-2"
        >
          {uploading ? (
            <>
              <Loader2 className="w-5 h-5 animate-spin" />
              <span>Uploading...</span>
            </>
          ) : (
            <>
              <Upload className="w-5 h-5" />
              <span>Upload Document</span>
            </>
          )}
        </button>
        <p className="text-white/60 text-sm text-center">PDF, DOCX, or TXT</p>
      </div>

      {/* Mode Toggle */}
      {documents.length > 0 && (
        <div className="bg-white/5 rounded-xl p-4 space-y-3">
          <label className="flex items-center gap-3 cursor-pointer">
            <input
              type="checkbox"
              checked={useKnowledgeBase}
              onChange={(e) => setUseKnowledgeBase(e.target.checked)}
              className="w-5 h-5 rounded accent-purple-600"
            />
            <div className="flex items-center gap-2 text-white">
              <BookOpen className="w-5 h-5" />
              <span className="font-medium">Use Knowledge Base</span>
            </div>
          </label>
          <p className="text-white/60 text-xs">
            {useKnowledgeBase 
              ? '✓ Answers will be based on uploaded documents' 
              : 'General chat mode'}
          </p>
        </div>
      )}

      {/* Documents List */}
      <div className="flex-1 overflow-y-auto space-y-2">
        <div className="flex items-center justify-between mb-2">
          <h3 className="text-white font-medium">Documents ({documents.length})</h3>
          {documents.length > 0 && (
            <button
              onClick={onDeleteAll}
              className="text-red-400 hover:text-red-300 transition-colors"
              title="Delete all documents"
            >
              <Trash2 className="w-4 h-4" />
            </button>
          )}
        </div>
        {documents.length === 0 ? (
          <div className="text-white/40 text-sm text-center py-8">
            No documents uploaded yet
          </div>
        ) : (
          documents.map((doc) => (
            <div key={doc.id} className="bg-white/10 rounded-lg p-3 flex items-start gap-3 group">
              <File className="w-5 h-5 text-purple-400 flex-shrink-0 mt-0.5" />
              <div className="flex-1 min-w-0">
                <p className="text-white text-sm font-medium truncate">{doc.filename}</p>
                <p className="text-white/60 text-xs">{doc.chunks} chunks</p>
              </div>
              <button
                onClick={() => onDeleteDocument(doc.id)}
                className="text-white/40 hover:text-red-400 transition-colors opacity-0 group-hover:opacity-100"
              >
                <X className="w-4 h-4" />
              </button>
            </div>
          ))
        )}
      </div>
    </div>
  );
}