import { Loader2, Bot } from "lucide-react";
import ChatMessage from "./ChatMessage";

interface MessageListProps {
  messages: { role: string; content: string }[];
  loading: boolean;
  messagesEndRef: React.RefObject<HTMLDivElement | null>;
}

export default function MessageList({ messages, loading, messagesEndRef }: MessageListProps) {
  return (
    <div className="flex-1 overflow-y-auto p-6 space-y-4">
      {messages.map((msg, idx) => (
        <ChatMessage key={idx} role={msg.role as "assistant" | "user"} content={msg.content} />
      ))}
      {loading && (
        <div className="flex gap-3 justify-start">
          <div className="bg-gradient-to-br from-purple-500 to-blue-500 p-2 rounded-full h-10 w-10 flex items-center justify-center">
            <Bot className="w-5 h-5 text-white" />
          </div>
          <div className="bg-white/20 text-white backdrop-blur-sm p-4 rounded-2xl flex items-center gap-2">
            <Loader2 className="w-4 h-4 animate-spin" />
            <span>Thinking...</span>
          </div>
        </div>
      )}
      <div ref={messagesEndRef} />
    </div>
  );
}
