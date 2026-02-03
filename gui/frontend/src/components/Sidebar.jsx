function Sidebar({
  chats = [],
  activeChatId,
  onNewChat,
  onSelectChat,
}) {
  return (
    <div style={styles.sidebar}>
      <button style={styles.newChat} onClick={onNewChat}>
        + New Chat
      </button>

      <div style={styles.chatList}>
        {chats.map((chat) => (
          <div
            key={chat.id}
            onClick={() => onSelectChat(chat.id)}
            style={{
              ...styles.chatItem,
              background:
                chat.id === activeChatId ? "#e5e7eb" : "transparent",
            }}
          >
            📄 {chat.title}
          </div>
        ))}
      </div>
    </div>
  );
}

const styles = {
  sidebar: {
    width: 240,
    borderRight: "1px solid #ddd",
    padding: 12,
    display: "flex",
    flexDirection: "column",
  },
  newChat: {
    width: "100%",
    marginBottom: 12,
    padding: 8,
    cursor: "pointer",
  },
  chatList: {
    display: "flex",
    flexDirection: "column",
    gap: 4,
  },
  chatItem: {
    padding: 8,
    borderRadius: 6,
    cursor: "pointer",
    fontSize: 14,
  },
};

export default Sidebar;
