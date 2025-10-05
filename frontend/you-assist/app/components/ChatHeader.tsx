import { Sparkles } from "lucide-react";

export default function ChatHeader() {
  return (
    <div className="bg-gradient-to-r from-purple-600 to-blue-600 p-6 flex items-center gap-3">
      <div className="bg-white/20 p-3 rounded-full">
        <Sparkles className="w-6 h-6 text-white" />
      </div>
      <div>
        <h1 className="text-2xl font-bold text-white">You Assist</h1>
        <p className="text-purple-100 text-sm">Running on your local LLM</p>
      </div>
    </div>
  );
}
