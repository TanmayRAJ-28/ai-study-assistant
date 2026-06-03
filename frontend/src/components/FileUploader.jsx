import { useState } from "react";
import { uploadPDFs } from "../api/client";

export default function FileUploader({
  setSessionId,
  setFileNames,
  selectedFile,
  setSelectedFile,
}) {
  const [files, setFiles] = useState([]);
  const [status, setStatus] = useState("");

  const handleUpload = async () => {
    try {
      const res = await uploadPDFs(files);
      setSessionId(res.session_id);
      if (Array.isArray(res.file_names)) {
        setFileNames((prev) => {
          const combined = [...prev];
          res.file_names.forEach((name) => {
            if (!combined.includes(name)) combined.push(name);
          });
          return combined;
        });

        if (!selectedFile && res.file_names.length > 0) {
          setSelectedFile(res.file_names[0]);
        }
      }
      setStatus("Uploaded successfully");
    } catch (err) {
      setStatus("Upload failed");
    }
  };

  return (
    <div className="p-4 border-r border-gray-700">
      <input
        type="file"
        multiple
        onChange={(e) => setFiles([...e.target.files])}
      />

      <div className="mt-2">
        {files.map((f, i) => (
          <div key={i} className="text-sm text-gray-300">
            {f.name}
          </div>
        ))}
      </div>

      <button
        onClick={handleUpload}
        className="mt-3 bg-green-600 px-4 py-2 rounded"
      >
        Upload
      </button>

      <div className="text-sm mt-2">{status}</div>
    </div>
  );
}