"use client";
import { useState, useRef, useEffect } from "react";

interface UseChatProps {
  useKnowledgeBase: boolean;
}

export function useChat({ useKnowledgeBase }: UseChatProps) {
  const [messages, setMessages] = useState([
    { role: "assistant", content: "Hello! I'm your AI assistant. How can I help you today?" },
  ]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement | null>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const sendMessage = async () => {
    if (!input.trim() || loading) return;

    const userMessage = { role: "user", content: input };
    setMessages((prev) => [...prev, userMessage]);
    setInput("");
    setLoading(true);

    try {
      const response = await fetch(`${process.env.NEXT_PUBLIC_API_SERVER}/api/v1/chat`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(
          { 
            message: userMessage.content, 
            history: messages,
            use_knowledge_base: useKnowledgeBase
          }
        ),
      });

      if (!response.ok) throw new Error("Failed to get response");
      const data = await response.json();

      setMessages((prev) => [...prev, { role: "assistant", content: data.response, sources: data.sources }]);
    } catch (err) {
      console.error(err);
      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          content: "Sorry, I encountered an error. Please make sure the backend server is running.",
        },
      ]);
    } finally {
      setLoading(false);
    }
  };
    
  const addSystemMessage = (content: string) => {
    setMessages(prev => [...prev, { role: 'assistant', content }]);
  };

  return { messages, input, setInput, loading, sendMessage, messagesEndRef, addSystemMessage };
}
