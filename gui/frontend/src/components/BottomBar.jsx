import ChatInputBar from "./ChatInputBar";

function BottomBar({
  query,
  setQuery,
  onSend,
  disabled,
  mode,
  setMode,
}) {
  return (
    <div style={styles.container}>
      <ChatInputBar
        query={query}
        setQuery={setQuery}
        onSend={onSend}
        disabled={disabled}
        mode={mode}
        setMode={setMode}
      />
    </div>
  );
}

const styles = {
  container: {
    borderTop: "1px solid #ffee00",
    padding: 10,
  },
};

export default BottomBar;
