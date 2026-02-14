import ModeDropdown from "./ModeDropdown";

function ChatInputBar({
  query,
  setQuery,
  onSend,
  disabled,
  mode,
  setMode,
}) {
  return (
<div style={styles.container}>
  <ModeDropdown mode={mode} setMode={setMode} />

  <textarea
    value={query}
    onChange={(e) => setQuery(e.target.value)}
    placeholder="Ask about the document…"
    disabled={disabled}
    style={styles.textarea}
  />

  <button disabled={disabled}>Send</button>
</div>
  );
}

const styles = {
container: {
  display: "flex",
  alignItems: "center",
  gap: 8,
  background: "#ffffff",
  padding: 8,
  borderRadius: 10,
},

textarea: {
  flex: 1,
  height: 40,
  background: "rgb(224 243 255)",
  color: "rgb(203 224 246)",
  border: "none",
  padding: "8px 10px",
  borderRadius: 8,
},

};

export default ChatInputBar;
