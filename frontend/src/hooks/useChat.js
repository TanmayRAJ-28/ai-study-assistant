import { useState } from "react";
import { queryStream } from "../api/client";

/**
 * useChat Hook
 * Handles chat state, streaming responses, and session management
 */
export default function useChat() {
  const [messages, setMessages] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const [sessionId, setSessionId] = useState(null);
  const [streamingText, setStreamingText] = useState("");
  const [fileNames, setFileNames] = useState([]);
  const [selectedFile, setSelectedFile] = useState(null);

  /**
   * Send user question to backend and handle SSE stream
   * @param {string} question
   */
  const sendMessage = async (question) => {
    if (!sessionId) {
      alert("Please upload PDF first");
      return;
    }

    if (!question.trim()) return;

    setIsLoading(true);
    setStreamingText("");

    // Add user message
    const userMessage = { role: "user", content: question };
    const updatedMessages = [...messages, userMessage];
    setMessages(updatedMessages);

    // ✅ Clean chat history (remove sources, keep only role + content)
    const cleanHistory = updatedMessages.map((msg) => ({
      role: msg.role,
      content: msg.content,
    }));

    let finalText = "";
    let sources = [];

    try {
      await queryStream(sessionId, question, cleanHistory, selectedFile, (data) => {
        // 🔹 Stream tokens
        if (data.token) {
          finalText += data.token + " ";
          setStreamingText((prev) => prev + data.token + " ");
        }

        // 🔹 Final sources
        if (data.sources) {
          sources = data.sources;
        }
      });

      // ✅ Add assistant message after stream ends
      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          content: finalText.trim(),
          sources,
        },
      ]);
    } catch (error) {
      console.error("Streaming error:", error);

      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          content: "⚠️ Error generating response. Please try again.",
        },
      ]);
    }

    setStreamingText("");
    setIsLoading(false);
  };

  /**
   * Clear chat history
   */
  const clearChat = () => {
    setMessages([]);
    setStreamingText("");
  };

  return {
    messages,
    isLoading,
    sessionId,
    setSessionId,
    streamingText,
    sendMessage,
    clearChat,
    fileNames,
    setFileNames,
    selectedFile,
    setSelectedFile,
  };
}