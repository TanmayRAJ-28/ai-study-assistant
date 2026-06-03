import { useState } from "react";

export default function SourceCitations({ sources }) {
  const [open, setOpen] = useState(false);

  return (
    <div className="mt-2">
      <button
        onClick={() => setOpen(!open)}
        className="text-xs text-blue-400"
      >
        {open ? "Hide Sources" : "Show Sources"}
      </button>

      {open && (
        <div className="mt-2 text-xs space-y-2">
          {sources.map((s, i) => (
            <div key={i} className="bg-gray-700 p-2 rounded">
              <div className="text-yellow-400">Page: {s.page}</div>
              <div>{s.excerpt}</div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}