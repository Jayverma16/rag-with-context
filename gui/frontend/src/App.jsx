import { useState } from "react";
import { chat, ingestFile } from "./services/api";
import UploadBox from "./components/UploadBox";
import Sidebar from "./components/Sidebar";
import BottomBar from "./components/BottomBar";


function App() {
  const [query, setQuery] = useState("");
  const [mode, setMode] = useState("hierarchy");
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(false);

  const [uploadedFile, setUploadedFile] = useState(null);
  const [uploadStatus, setUploadStatus] = useState("");
  const [ingestStatus, setIngestStatus] = useState("");

  // 🔑 Chat history state (basic for now)
  const [chats, setChats] = useState([
    { id: "1", title: "Banking Law" },
    { id: "2", title: "Tax Code" },
  ]);
  const [activeChatId, setActiveChatId] = useState("1");

  const runQuery = async () => {
    if (!query.trim()) return;

    setMessages((m) => [...m, { role: "user", content: query }]);
    setQuery("");
    setLoading(true);

    try {
      const res = await chat(query, mode);
      setMessages((m) => [
        ...m,
        { role: "assistant", content: res.answer },
      ]);
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
      {/* ========== LEFT SIDEBAR ========== */}
      <Sidebar
        chats={chats}
        activeChatId={activeChatId}
        onNewChat={() => {
          const id = Date.now().toString();
          setChats((c) => [
            { id, title: "New Chat" },
            ...c,
          ]);
          setActiveChatId(id);
          setMessages([]);
          setUploadedFile(null);
          setIngestStatus("");
        }}
        onSelectChat={(id) => {
          setActiveChatId(id);
          setMessages([]);
        }}
      />

    {/* ========== CENTER ========== */}

      {/* Upload state (centered perfectly) */}
      <div style={styles.center}>

      
      {!uploadedFile && (
        <div style={styles.uploadWrapper}>
          <UploadBox
            uploadStatus={uploadStatus}
            setUploadStatus={setUploadStatus}
            onUploadSuccess={setUploadedFile}
          />
        </div>
      )}

        <div style={styles.bottomBar}>
          <BottomBar
            query={query}
            setQuery={setQuery}
            onSend={runQuery}
            disabled={!ingestStatus.startsWith("✅") || loading}
            mode={mode}
            setMode={setMode}
          />
        </div>
        </div>
</div>)
}


  


/* styles */
const styles = {
  app: { display: "flex", height: "100vh", fontFamily: "sans-serif" },
  center: { flex: 1, display: "flex", flexDirection: "column" },
  bottomBar: {  padding: 16, overflowY: "auto" ,  bottom: 0, },
  message: { padding: 10, borderRadius: 8, background: "#f3f4f6", maxWidth: "70%" },
  // bottomBar: { borderTop: "1px solid #ddd", padding: 10 },
  inputBox: { display: "flex", gap: 8, marginTop: 8 },
  uploadBox: {
  margin: "auto",
  textAlign: "center",
},
  uploadWrapper: {
  flex: 1,
  display: "flex",
  alignItems: "center",     // vertical center ✅
  justifyContent: "center" // horizontal center ✅
}
};

export default App;
