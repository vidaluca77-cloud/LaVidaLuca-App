"use client";
import React, { useState } from "react";

export default function TestIA() {
  const [q, setQ] = useState("Comment améliorer un sol argileux compact ?");
  const [res, setRes] = useState("");
  const [loading, setLoading] = useState(false);

  const api = process.env.NEXT_PUBLIC_IA_API_URL || "http://127.0.0.1:8001";

  async function ask(e: React.FormEvent) {
    e.preventDefault();
    setLoading(true);
    setRes("");
    try {
      const r = await fetch(`${api}/chat`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ question: q }),
      });
      if (!r.ok) {
        const txt = await r.text();
        throw new Error(`HTTP ${r.status} - ${txt}`);
      }
      const data = await r.json();
      setRes(data.answer ?? JSON.stringify(data));
    } catch (err: any) {
      setRes(`Erreur: ${err.message}`);
    } finally {
      setLoading(false);
    }
  }

  return (
    <main style={{ padding: 24, maxWidth: 900, margin: "0 auto" }}>
      <h1 style={{ fontWeight: 800, fontSize: 28 }}>Test liaison IA</h1>
      <div style={{ marginTop: 8, color: "#555" }}>API: {api}</div>

      <form onSubmit={ask} style={{ marginTop: 16, display: "flex", gap: 8 }}>
        <input
          value={q}
          onChange={(e) => setQ(e.target.value)}
          style={{ flex: 1, padding: 10, border: "1px solid #ddd" }}
          placeholder="Pose ta question…"
        />
        <button disabled={loading} type="submit" style={{ padding: "10px 16px" }}>
          {loading ? "Patiente…" : "Poser la question"}
        </button>
      </form>

      <pre style={{ marginTop: 16, background: "#f7f7f7", padding: 12, whiteSpace: "pre-wrap" }}>
        {res || "—"}
      </pre>
    </main>
  );
}
