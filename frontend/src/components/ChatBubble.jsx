import SourceCitations from "./SourceCitations";

export default function ChatBubble({ message, isStreaming }) {
  return (
    <div
      className={`p-3 rounded-xl max-w-lg ${
        message.role === "user"
          ? "bg-blue-600 text-white self-end"
          : "bg-gray-800 text-white self-start"
      }`}
    >
      <div>
        {message.content}
        {isStreaming && <span className="animate-pulse"> |</span>}
      </div>

      {message.sources && <SourceCitations sources={message.sources} />}
    </div>
  );
}