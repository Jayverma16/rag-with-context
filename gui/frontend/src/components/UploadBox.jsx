import UploadIcon from "../assets/file_upload_logo.png";
import { uploadFile } from "../services/api";

function UploadBox({
  onUploadSuccess,
  uploadStatus,
  setUploadStatus,
}) {
  return (
    <div style={styles.uploadBox}>
      <img src={UploadIcon} alt="Upload" style={styles.icon} />

      <h3>Upload legal document</h3>

      <label style={styles.uploadLabel}>
        Click to upload
        <input
          type="file"
          hidden
          accept=".pdf,.txt,.md"
          onChange={async (e) => {
            const file = e.target.files[0];
            e.target.value = "";
            if (!file) return;

            setUploadStatus("Uploading...");
            try {
              const res = await uploadFile(file);
              setUploadStatus(`Uploaded: ${res.filename}`);
              onUploadSuccess(res.filename); // 🔑 send filename to parent
            } catch (err) {
              console.error(err);
              setUploadStatus("❌ Upload failed");
            }
          }}
        />
      </label>

      <small style={styles.status}>{uploadStatus}</small>
    </div>
  );
}

const styles = {
  uploadBox: {
    margin: "auto",
    textAlign: "center",
  },
  icon: {
    width: 90,
    marginBottom: 12,
    opacity: 0.9,
  },
  uploadLabel: {
    cursor: "pointer",
    color: "#2563eb",
    fontWeight: 500,
  },
  status: {
    display: "block",
    marginTop: 8,
    fontSize: 13,
    color: "#555",
  },
};

export default UploadBox;
