import Lottie from "lottie-react";
import UploadIcon from "../assets/file_upload_logo.png";
import uploadingAnimation from "../assets/Uploading.json";
import { uploadFile } from "../services/api";

function UploadBox({
  onUploadSuccess,
  uploadStatus,
  setUploadStatus,
}) {
  const isUploading = uploadStatus.startsWith("Uploading");

  return (
    <div style={styles.uploadBox}>
      {/* 🔄 ICON ↔ ANIMATION */}
      {!isUploading ? (
        <img
          src={UploadIcon}
          alt="Upload"
          style={styles.icon}
        />
      ) : (
        <Lottie
          animationData={uploadingAnimation}
          loop
          style={styles.lottie}
        />
      )}

      <h3>
        {isUploading ? "Uploading document…" : "Upload legal document"}
      </h3>

      {!isUploading && (
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
                onUploadSuccess(res.filename);
              } catch (err) {
                console.error(err);
                setUploadStatus("❌ Upload failed");
              }
            }}
          />
        </label>
      )}

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
  lottie: {
    width: 120,
    height: 120,
    margin: "0 auto 12px",
  },
  uploadLabel: {
    cursor: "pointer",
    color: "#3b82f6",
    fontWeight: 500,
  },
  status: {
    display: "block",
    marginTop: 8,
    fontSize: 13,
    opacity: 0.8,
  },
};

export default UploadBox