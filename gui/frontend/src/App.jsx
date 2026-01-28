import { useState } from "react";
import { chat, uploadFile, ingestFile } from "./services/api";

function App() {
  const [query, setQuery] = useState("");
  const [mode, setMode] = useState("hierarchy");
  const [answer, setAnswer] = useState("");
  const [chunks, setChunks] = useState([]);
  const [loading, setLoading] = useState(false);

  const [uploadStatus, setUploadStatus] = useState("");
  const [uploadedFile, setUploadedFile] = useState(null);
  const [ingestStatus, setIngestStatus] = useState("");

  const runQuery = async () => {
    if (!query.trim()) return;

    setLoading(true);
    try {
      const res = await chat(query, mode);
      setAnswer(res.answer);
      setChunks(res.chunks);
    } catch (err) {
      setAnswer("❌ Error calling backend");
      setChunks([]);
    }
    setLoading(false);
  };

  return (
    <div style={{ padding: 24, fontFamily: "sans-serif", maxWidth: 900 }}>
      <h2>🧠 RAG Inspector</h2>

      {/* ================= Upload ================= */}
      <div style={{ marginBottom: 20 }}>
        <strong>Upload document</strong><br />
        <input
          type="file"
          accept=".pdf,.txt,.md"
          onChange={async (e) => {
            const file = e.target.files[0];
            e.target.value = ""; // 🔑 reset input
            if (!file) return;

            setUploadStatus("Uploading...");
            setUploadedFile(null);
            setIngestStatus("");

            try {
              const res = await uploadFile(file);
              setUploadedFile(res.filename); // 🔑 store filename
              setUploadStatus(`✅ Uploaded: ${res.filename}`);
            } catch (err) {
              console.error(err);
              setUploadStatus("❌ Upload failed");
            }
          }}
        />
        <div style={{ fontSize: 13, marginTop: 4 }}>
          {uploadStatus}
        </div>
      </div>

      {/* ================= Ingest ================= */}
      {uploadedFile && (
        <div style={{ marginBottom: 20 }}>
          <button
            onClick={async () => {
              setIngestStatus("Ingesting...");
              try {
                await ingestFile(uploadedFile);
                setIngestStatus("✅ Ingestion complete. You can now ask questions.");
              } catch (err) {
                console.error(err);
                setIngestStatus("❌ Ingestion failed");
              }
            }}
          >
            Ingest document
          </button>
          <div style={{ fontSize: 13, marginTop: 4 }}>
            {ingestStatus}
          </div>
        </div>
      )}

      {/* ================= Query ================= */}
      <textarea
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        placeholder="Ask a question..."
        style={{ width: "100%", height: 80 }}
        disabled={!ingestStatus.startsWith("✅")}
      />

      <div style={{ marginTop: 10 }}>
        <label>
          <input
            type="radio"
            checked={mode === "flat"}
            onChange={() => setMode("flat")}
          />
          Flat
        </label>

        <label style={{ marginLeft: 20 }}>
          <input
            type="radio"
            checked={mode === "hierarchy"}
            onChange={() => setMode("hierarchy")}
          />
          Hierarchy-aware
        </label>
      </div>

      <button
        onClick={runQuery}
        disabled={loading || !ingestStatus.startsWith("✅")}
        style={{ marginTop: 10 }}
      >
        {loading ? "Thinking..." : "Ask"}
      </button>

      <hr />

      {/* ================= Answer ================= */}
      <h3>Answer</h3>
      <div style={{ background: "#f5f5f5", padding: 12 }}>
        {answer || "—"}
      </div>

      {/* ================= Chunks ================= */}
      <h3>Retrieved Chunks</h3>
      {chunks.map((c, i) => (
        <div
          key={i}
          style={{
            border: "1px solid #ddd",
            marginBottom: 10,
            padding: 10,
          }}
        >
          <strong>Metadata</strong>
          <pre>{JSON.stringify(c.metadata, null, 2)}</pre>

          <strong>Content</strong>
          <pre style={{ whiteSpace: "pre-wrap" }}>{c.content}</pre>
        </div>
      ))}
    </div>
  );
}

export default App;
