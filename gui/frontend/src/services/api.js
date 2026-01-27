export async function chat(query, mode) {
  const res = await fetch("http://127.0.0.1:8000/chat", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ query, mode }),
  });

  if (!res.ok) {
    throw new Error("API error");
  }

  return res.json();
}
