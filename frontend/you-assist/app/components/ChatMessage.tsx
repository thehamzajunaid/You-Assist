import { Bot, User } from "lucide-react";

interface ChatMessageProps {
  role: "assistant" | "user";
  content: string;
}

export default function ChatMessage({ role, content }: ChatMessageProps) {
  const isUser = role === "user";
  return (
    <div className={`flex gap-3 ${isUser ? "justify-end" : "justify-start"}`}>
      {!isUser && (
        <div className="bg-gradient-to-br from-purple-500 to-blue-500 p-2 rounded-full h-10 w-10 flex items-center justify-center flex-shrink-0">
          <Bot className="w-5 h-5 text-white" />
        </div>
      )}
      <div
        className={`max-w-[70%] p-4 rounded-2xl ${
          isUser
            ? "bg-gradient-to-r from-purple-600 to-blue-600 text-white"
            : "bg-white/20 text-white backdrop-blur-sm"
        }`}
      >
        <p className="whitespace-pre-wrap break-words">{content}</p>
      </div>
      {isUser && (
        <div className="bg-gradient-to-br from-green-500 to-emerald-500 p-2 rounded-full h-10 w-10 flex items-center justify-center flex-shrink-0">
          <User className="w-5 h-5 text-white" />
        </div>
      )}
    </div>
  );
}
