import { useState } from "react";

export default function QueryInput({ onSend, disabled }) {
  const [text, setText] = useState("");

  const handleSend = () => {
    if (!text.trim()) return;
    onSend(text);
    setText("");
  };

  return (
    <div className="p-3 border-t border-gray-700 flex gap-2">
      <input
        className="flex-1 p-2 bg-gray-800 text-white rounded"
        value={text}
        onChange={(e) => setText(e.target.value)}
        disabled={disabled}
        onKeyDown={(e) => e.key === "Enter" && handleSend()}
      />
      <button
        onClick={handleSend}
        disabled={disabled}
        className="bg-blue-600 px-4 rounded"
      >
        Send
      </button>
    </div>
  );
}