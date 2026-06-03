import useChat from "./hooks/useChat";
import FileUploader from "./components/FileUploader";
import ChatWindow from "./components/ChatWindow";
import QueryInput from "./components/QueryInput";

export default function App() {
  const {
    messages,
    isLoading,
    sessionId,
    setSessionId,
    streamingText,
    sendMessage,
    fileNames,
    setFileNames,
    selectedFile,
    setSelectedFile,
  } = useChat();

  return (
    <div className="h-screen flex bg-gray-900 text-white">
      <div className="w-1/4">
        <FileUploader
          setSessionId={setSessionId}
          setFileNames={setFileNames}
          selectedFile={selectedFile}
          setSelectedFile={setSelectedFile}
        />
      </div>

      <div className="flex flex-col flex-1">
        <div className="p-3 border-b border-gray-700 flex items-center justify-between gap-4">
          <h1 className="text-xl font-bold">AI Study Assistant</h1>

          {fileNames.length > 0 && (
            <div className="flex items-center gap-2 text-sm">
              <span className="text-gray-300">Ask about:</span>
              <select
                className="bg-gray-800 text-white rounded px-2 py-1 text-sm"
                value={selectedFile || ""}
                onChange={(e) =>
                  setSelectedFile(e.target.value || null)
                }
              >
                <option value="">All files</option>
                {fileNames.map((name) => (
                  <option key={name} value={name}>
                    {name}
                  </option>
                ))}
              </select>
            </div>
          )}
        </div>

        <ChatWindow
          messages={messages}
          streamingText={streamingText}
        />

        <QueryInput onSend={sendMessage} disabled={isLoading} />
      </div>
    </div>
  );
}