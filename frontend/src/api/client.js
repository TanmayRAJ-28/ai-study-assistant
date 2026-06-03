import axios from "axios";

const API_BASE =
  "https://ai-study-assistant-backend-p4vb.onrender.com/api";

export const uploadPDFs = async (files, sessionId = null) => {
  const formData = new FormData();

  files.forEach((file) => formData.append("files", file));
  if (sessionId) formData.append("session_id", sessionId);

  const res = await axios.post(`${API_BASE}/upload`, formData, {
    headers: { "Content-Type": "multipart/form-data" },
  });

  return res.data;
};

// ⚠️ Using fetch streaming instead of EventSource (POST required)
export const queryStream = async (
  sessionId,
  question,
  chatHistory,
  fileName,
  onMessage
) => {
  const res = await fetch(`${API_BASE}/query`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      session_id: sessionId,
      question,
      chat_history: chatHistory,
      file_name: fileName || null,
    }),
  });

  const reader = res.body.getReader();
  const decoder = new TextDecoder();

  while (true) {
    const { done, value } = await reader.read();
    if (done) break;

    const chunk = decoder.decode(value, { stream: true });

    chunk.split("\n\n").forEach((line) => {
      if (line.startsWith("data: ")) {
        const data = JSON.parse(line.replace("data: ", ""));
        onMessage(data);
      }
    });
  }
};
