function ModeDropdown({ mode, setMode }) {
  return (
    <select
      value={mode}
      onChange={(e) => setMode(e.target.value)}
      style={styles.select}
    >
      <option value="flat" style={{ color: "#011f4e" }} >Flat</option>
      <option value="hierarchy" style={{ color: "#011f4e" }} >Hierarchy</option>
    </select>
  );
}

const styles = {
  select: {
    height: 40,
    padding: "0 10px",
    borderRadius: 6,
    border: "1px solid #000000",
    background: "#d9ff00",
    fontSize: 14,
    cursor: "pointer",
  },
};

export default ModeDropdown;
