import { useEffect, useRef } from "react";
import ChatBubble from "./ChatBubble";

export default function ChatWindow({ messages, streamingText }) {
  const bottomRef = useRef();

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, streamingText]);

  return (
    <div className="flex-1 p-4 overflow-y-auto flex flex-col gap-3">
      {messages.length === 0 && (
        <div className="text-gray-500">Start chatting...</div>
      )}

      {messages.map((msg, i) => (
        <ChatBubble key={i} message={msg} />
      ))}

      {streamingText && (
        <ChatBubble
          message={{ role: "assistant", content: streamingText }}
          isStreaming
        />
      )}

      <div ref={bottomRef} />
    </div>
  );
}