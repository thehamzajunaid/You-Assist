"use client";
import ChatHeader from "./components/ChatHeader";
import MessageList from "./components/MessageList";
import ChatInput from "./components/ChatInput";
import { useChat } from "./hooks/useChat";
import { useDocuments } from "./hooks/useDocuments";
import Sidebar from "./components/Sidebar";

export default function AIAssistantPage() {
  const {
    documents,
    uploading,
    useKnowledgeBase,
    setUseKnowledgeBase,
    uploadDocument,
    deleteDocument,
    deleteAllDocuments,
  } = useDocuments();

  const { messages, input, setInput, loading, sendMessage, messagesEndRef, addSystemMessage } = useChat({useKnowledgeBase});

  const handleUpload = async (file: File) => {
    const message = await uploadDocument(file);
    if (message) {
      addSystemMessage(message);
    }
  };

  const handleDeleteDocument = async (id: string) => {
    const message = await deleteDocument(id);
    if (message) {
      addSystemMessage(message);
    }
  };

  const handleDeleteAll = async () => {
    const message = await deleteAllDocuments();
    if (message) {
      addSystemMessage(message);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900 flex items-center justify-center p-4">
      {/* Sidebar */}
      <Sidebar
        documents={documents}
        useKnowledgeBase={useKnowledgeBase}
        setUseKnowledgeBase={setUseKnowledgeBase}
        onUpload={handleUpload}
        onDeleteDocument={handleDeleteDocument}
        onDeleteAll={handleDeleteAll}
        uploading={uploading}
      />
      <div className="w-full max-w-4xl h-[90vh] bg-white/10 backdrop-blur-lg rounded-2xl shadow-2xl border border-white/20 flex flex-col overflow-hidden">
        <ChatHeader />
        <MessageList messages={messages} loading={loading} messagesEndRef={messagesEndRef} />
        <ChatInput input={input} setInput={setInput} onSubmit={sendMessage} loading={loading} />
      </div>
    </div>
  );
}
