"use client";
import ChatHeader from "./components/ChatHeader";
import MessageList from "./components/MessageList";
import ChatInput from "./components/ChatInput";
import { useChat } from "./hooks/useChat";

export default function AIAssistantPage() {
  const { messages, input, setInput, loading, sendMessage, messagesEndRef } = useChat();

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900 flex items-center justify-center p-4">
      <div className="w-full max-w-4xl h-[90vh] bg-white/10 backdrop-blur-lg rounded-2xl shadow-2xl border border-white/20 flex flex-col overflow-hidden">
        <ChatHeader />
        <MessageList messages={messages} loading={loading} messagesEndRef={messagesEndRef} />
        <ChatInput input={input} setInput={setInput} onSubmit={sendMessage} loading={loading} />
      </div>
    </div>
  );
}
