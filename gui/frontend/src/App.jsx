import { useState } from "react";
import { chat, uploadFile, ingestFile } from "./services/api";
import UploadIcon from "./assets/file_upload_logo.png";
  

function App() {
  const [query, setQuery] = useState("");
  const [mode, setMode] = useState("hierarchy");
  const [messages, setMessages] = useState([]);
  const [chunks, setChunks] = useState([]);
  const [loading, setLoading] = useState(false);

  const [uploadStatus, setUploadStatus] = useState("");
  const [uploadedFile, setUploadedFile] = useState(null);
  const [ingestStatus, setIngestStatus] = useState("");

  const runQuery = async () => {
    if (!query.trim()) return;

    const userMsg = { role: "user", content: query };
    setMessages((m) => [...m, userMsg]);
    setQuery("");
    setLoading(true);

    try {
      const res = await chat(userMsg.content, mode);
      setMessages((m) => [
        ...m,
        { role: "assistant", content: res.answer },
      ]);
      setChunks(res.chunks);
    } catch {
      setMessages((m) => [
        ...m,
        { role: "assistant", content: "❌ Error calling backend" },
      ]);
    }
    setLoading(false);
  };

  return (
    <div style={styles.app}>
      {/* ================= CENTER ================= */}
      <div style={styles.center}>
        {/* Upload state */}
        {!uploadedFile && (
<div style={styles.uploadBox}>
  <img
    src={UploadIcon}
    alt="Upload"
    style={{ width: 96, opacity: 0.9, marginBottom: 12 }}
  />

  <h2>Upload legal document</h2>

  <label style={{ cursor: "pointer", color: "#555" }}>
    Click to browse or drag & drop
    <input
      type="file"
      accept=".pdf,.txt,.md"
      hidden
      onChange={async (e) => {
        const file = e.target.files[0];
        e.target.value = "";
        if (!file) return;

        setUploadStatus("Uploading...");
        try {
          const res = await uploadFile(file);
          setUploadedFile(res.filename);
          setUploadStatus(`Uploaded: ${res.filename}`);
        } catch {
          setUploadStatus("❌ Upload failed");
        }
      }}
    />
  </label>

  <small style={{ marginTop: 8, display: "block" }}>
    {uploadStatus}
  </small>
</div>
        )}

        {/* Chat messages */}
        <div style={styles.chatArea}>
          {messages.map((m, i) => (
            <div
              key={i}
              style={{
                ...styles.message,
                alignSelf: m.role === "user" ? "flex-end" : "flex-start",
                background: m.role === "user" ? "#daf" : "#eee",
              }}
            >
              {m.content}
            </div>
          ))}
          {loading && <div style={styles.message}>Thinking…</div>}
        </div>

        {/* ================= INPUT ================= */}
        <div style={styles.inputBar}>
          <textarea
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="Ask about the document…"
            disabled={!ingestStatus.startsWith("✅")}
            style={styles.textarea}
          />

          <button
            onClick={runQuery}
            disabled={loading || !ingestStatus.startsWith("✅")}
          >
            Send
          </button>
        </div>
      </div>

      {/* ================= RIGHT SIDEBAR ================= */}
      <div style={styles.sidebar}>
        <button
          onClick={async () => {
            setIngestStatus("Ingesting...");
            try {
              await ingestFile(uploadedFile);
              setIngestStatus("✅ Ready");
            } catch {
              setIngestStatus("❌ Ingest failed");
            }
          }}
          disabled={!uploadedFile}
        >
          Ingest
        </button>

        <div style={{ marginTop: 10 }}>
          <label>
            <input
              type="radio"
              checked={mode === "flat"}
              onChange={() => setMode("flat")}
            />{" "}
            Flat
          </label>
          <br />
          <label>
            <input
              type="radio"
              checked={mode === "hierarchy"}
              onChange={() => setMode("hierarchy")}
            />{" "}
            Hierarchy
          </label>
        </div>

        <small>{ingestStatus}</small>
      </div>
    </div>
  );
}

/* ================= STYLES ================= */

const styles = {
  app: {
    display: "flex",
    height: "100vh",
    fontFamily: "sans-serif",
  },
  center: {
    flex: 1,
    display: "flex",
    flexDirection: "column",
  },
  uploadBox: {
    margin: "auto",
    textAlign: "center",
  },
  chatArea: {
    flex: 1,
    padding: 20,
    overflowY: "auto",
    display: "flex",
    flexDirection: "column",
    gap: 10,
  },
  message: {
    maxWidth: "70%",
    padding: 10,
    borderRadius: 8,
  },
  inputBar: {
    display: "flex",
    gap: 10,
    padding: 10,
    borderTop: "1px solid #ddd",
  },
  textarea: {
    flex: 1,
    height: 60,
  },
  sidebar: {
    width: 260,
    borderLeft: "1px solid #ddd",
    padding: 16,
  },
};

export default App;
