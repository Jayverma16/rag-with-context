const API_BASE = import.meta.env.VITE_API_BASE_URL || "http://127.0.0.1:8000";

async function request(path, options = {}) {
  const res = await fetch(`${API_BASE}${path}`, options);
  if (!res.ok) {
    const detail = await res.text();
    throw new Error(detail || "API request failed");
  }
  return res.json();
}

export function listDocuments() {
  return request("/documents");
}

export function uploadDocuments(files) {
  const formData = new FormData();
  Array.from(files).forEach((file) => formData.append("files", file));
  return request("/documents/upload", {
    method: "POST",
    body: formData,
  });
}

export function ingestDocument(documentId) {
  return request(`/documents/${documentId}/ingest`, {
    method: "POST",
  });
}

export function loadChunks(documentId) {
  return request(`/documents/${documentId}/chunks`);
}

export function chat({ question, documentIds, mode, topK }) {
  return request("/chat", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      question,
      document_ids: documentIds,
      mode,
      top_k: topK,
    }),
  });
}
