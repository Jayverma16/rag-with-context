function ModeSelector({ mode, setMode }) {
  return (
    <div style={styles.container}>
      <label>
        <input
          type="radio"
          checked={mode === "flat"}
          onChange={() => setMode("flat")}
        />{" "}
        Flat
      </label>

      <label style={{ marginLeft: 12 }}>
        <input
          type="radio"
          checked={mode === "hierarchy"}
          onChange={() => setMode("hierarchy")}
        />{" "}
        Hierarchy
      </label>
    </div>
  );
}

const styles = {
  container: {
    display: "flex",
    alignItems: "center",
    fontSize: 14,
  },
};

export default ModeSelector;
