import { useEffect, useMemo, useState } from "react";
import "./App.css";
import {
  chat,
  ingestDocument,
  listDocuments,
  loadChunks,
  uploadDocuments,
} from "./services/api";

function App() {
  const [documents, setDocuments] = useState([]);
  const [selectedIds, setSelectedIds] = useState([]);
  const [question, setQuestion] = useState("");
  const [mode, setMode] = useState("hierarchy");
  const [topK, setTopK] = useState(5);
  const [messages, setMessages] = useState([]);
  const [sources, setSources] = useState([]);
  const [debugChunks, setDebugChunks] = useState([]);
  const [activeDebugDoc, setActiveDebugDoc] = useState("");
  const [busy, setBusy] = useState("");
  const [error, setError] = useState("");

  const readyDocuments = useMemo(
    () => documents.filter((document) => document.status === "ready"),
    [documents],
  );

  async function refreshDocuments() {
    const data = await listDocuments();
    setDocuments(data);
  }

  useEffect(() => {
    refreshDocuments().catch((err) => setError(err.message));
  }, []);

  async function handleUpload(event) {
    const files = event.target.files;
    event.target.value = "";
    if (!files.length) return;

    setBusy("Uploading PDFs");
    setError("");
    try {
      await uploadDocuments(files);
      await refreshDocuments();
    } catch (err) {
      setError(err.message);
    } finally {
      setBusy("");
    }
  }

  async function handleIngest(documentId) {
    setBusy(`Ingesting ${documentId}`);
    setError("");
    try {
      await ingestDocument(documentId);
      await refreshDocuments();
    } catch (err) {
      setError(err.message);
      await refreshDocuments().catch(() => {});
    } finally {
      setBusy("");
    }
  }

  async function handleDebug(documentId) {
    if (!documentId) {
      setDebugChunks([]);
      setActiveDebugDoc("");
      return;
    }
    setActiveDebugDoc(documentId);
    setError("");
    try {
      const data = await loadChunks(documentId);
      setDebugChunks(data.slice(0, 12));
    } catch (err) {
      setError(err.message);
    }
  }

  function toggleDocument(documentId) {
    setSelectedIds((current) =>
      current.includes(documentId)
        ? current.filter((id) => id !== documentId)
        : [...current, documentId],
    );
  }

  async function askQuestion(event) {
    event.preventDefault();
    const cleanQuestion = question.trim();
    if (!cleanQuestion) return;

    const selectedReadyIds = selectedIds.filter((id) =>
      readyDocuments.some((document) => document.id === id),
    );

    setMessages((current) => [
      ...current,
      { role: "user", content: cleanQuestion },
    ]);
    setQuestion("");
    setBusy("Answering");
    setError("");
    try {
      const response = await chat({
        question: cleanQuestion,
        documentIds: selectedReadyIds.length ? selectedReadyIds : null,
        mode,
        topK,
      });
      setMessages((current) => [
        ...current,
        { role: "assistant", content: response.answer },
      ]);
      setSources(response.sources || []);
    } catch (err) {
      setError(err.message);
    } finally {
      setBusy("");
    }
  }

  const allReadySelected =
    readyDocuments.length > 0 &&
    readyDocuments.every((document) => selectedIds.includes(document.id));

  return (
    <main className="appShell">
      <section className="documentPane">
        <div className="paneHeader">
          <div>
            <p className="eyebrow">rag-with-context</p>
            <h1>Document RAG</h1>
          </div>
          <label className="uploadButton">
            Upload PDFs
            <input type="file" accept=".pdf" multiple onChange={handleUpload} />
          </label>
        </div>

        <div className="selectionBar">
          <button
            type="button"
            onClick={() =>
              setSelectedIds(allReadySelected ? [] : readyDocuments.map((doc) => doc.id))
            }
            disabled={!readyDocuments.length}
          >
            {allReadySelected ? "Clear" : "Select all ready"}
          </button>
          <span>{selectedIds.length || "All ready"} document scope</span>
        </div>

        <div className="documentList">
          {documents.length === 0 && (
            <p className="emptyState">Upload PDFs to start building the corpus.</p>
          )}
          {documents.map((document) => (
            <article className="documentRow" key={document.id}>
              <label>
                <input
                  type="checkbox"
                  checked={selectedIds.includes(document.id)}
                  disabled={document.status !== "ready"}
                  onChange={() => toggleDocument(document.id)}
                />
                <span>{document.filename}</span>
              </label>
              <div className="rowActions">
                <span className={`status ${document.status}`}>{document.status}</span>
                <button
                  type="button"
                  onClick={() => handleIngest(document.id)}
                  disabled={busy || document.status === "processing"}
                >
                  Ingest
                </button>
                <button type="button" onClick={() => handleDebug(document.id)}>
                  Chunks
                </button>
              </div>
            </article>
          ))}
        </div>
      </section>

      <section className="chatPane">
        <div className="toolbar">
          <label>
            Mode
            <select value={mode} onChange={(event) => setMode(event.target.value)}>
              <option value="hierarchy">Hierarchy</option>
              <option value="flat">Flat</option>
            </select>
          </label>
          <label>
            Top K
            <input
              type="number"
              min="1"
              max="20"
              value={topK}
              onChange={(event) => setTopK(Number(event.target.value))}
            />
          </label>
          {busy && <span className="busy">{busy}</span>}
        </div>

        <div className="messages">
          {messages.length === 0 && (
            <p className="emptyState">
              Ask across all ready documents, or select specific PDFs on the left.
            </p>
          )}
          {messages.map((message, index) => (
            <div className={`message ${message.role}`} key={`${message.role}-${index}`}>
              {message.content}
            </div>
          ))}
        </div>

        <form className="askForm" onSubmit={askQuestion}>
          <textarea
            value={question}
            onChange={(event) => setQuestion(event.target.value)}
            placeholder="Ask a grounded question about your uploaded documents"
          />
          <button type="submit" disabled={busy || !readyDocuments.length}>
            Ask
          </button>
        </form>

        {error && <p className="error">{error}</p>}

        <section className="sources">
          <h2>Sources</h2>
          {sources.length === 0 && <p className="emptyState">Citations appear after an answer.</p>}
          {sources.map((source, index) => (
            <article className="sourceItem" key={`${source.document_id}-${index}`}>
              <header>
                <strong>{source.filename}</strong>
                <span>
                  Page {source.page_number} · {source.score.toFixed(3)}
                </span>
              </header>
              <p>{source.chunk_text}</p>
            </article>
          ))}
        </section>
      </section>

      <aside className="debugPane">
        <h2>Debug Chunks</h2>
        {!activeDebugDoc && <p className="emptyState">Choose Chunks on a document.</p>}
        {debugChunks.map((chunk) => (
          <article className="debugChunk" key={chunk.id}>
            <header>
              <strong>#{chunk.chunk_index}</strong>
              <span>Page {chunk.page_number}</span>
            </header>
            <p>{chunk.text}</p>
          </article>
        ))}
      </aside>
    </main>
  );
}

export default App;
