"use client";
import React, { useState } from "react";

export default function TestIA() {
  const [q, setQ] = useState("Comment améliorer un sol argileux compact ?");
  const [res, setRes] = useState("");
  const [loading, setLoading] = useState(false);

  const api = process.env.NEXT_PUBLIC_API_URL || "http://127.0.0.1:8000/api/v1";

  async function ask(e: React.FormEvent) {
    e.preventDefault();
    setLoading(true);
    setRes("");
    try {
      const r = await fetch(`${api}/guide`, {
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
      <h1 style={{ fontWeight: 800, fontSize: 28 }}>Test API Guide</h1>
      <div style={{ marginTop: 8, color: "#555" }}>API: {api}</div>
      <div style={{ marginTop: 4, color: "#777", fontSize: 14 }}>
        Cette page teste l'endpoint /guide de l'API principale La Vida Luca
      </div>

      <form onSubmit={ask} style={{ marginTop: 16, display: "flex", gap: 8 }}>
        <input
          value={q}
          onChange={(e) => setQ(e.target.value)}
          style={{ flex: 1, padding: 10, border: "1px solid #ddd", borderRadius: 4 }}
          placeholder="Pose ta question sur le jardinage, la permaculture..."
        />
        <button 
          disabled={loading} 
          type="submit" 
          style={{ 
            padding: "10px 16px", 
            backgroundColor: loading ? "#ccc" : "#007bff",
            color: "white",
            border: "none",
            borderRadius: 4,
            cursor: loading ? "not-allowed" : "pointer"
          }}
        >
          {loading ? "Traitement..." : "Poser la question"}
        </button>
      </form>

      <div style={{ marginTop: 16 }}>
        <h3>Réponse :</h3>
        <pre style={{ 
          background: "#f7f7f7", 
          padding: 12, 
          whiteSpace: "pre-wrap",
          borderRadius: 4,
          border: "1px solid #ddd",
          minHeight: 100
        }}>
          {res || "Posez une question pour recevoir une réponse personnalisée..."}
        </pre>
      </div>
      
      <div style={{ marginTop: 20, padding: 16, background: "#f0f8ff", borderRadius: 4 }}>
        <h4>Exemples de questions :</h4>
        <ul style={{ margin: 0, paddingLeft: 20 }}>
          <li>Comment améliorer un sol argileux compact ?</li>
          <li>Quelles plantes pour débuter un potager ?</li>
          <li>Comment faire du compost rapidement ?</li>
          <li>Techniques de permaculture pour petit jardin</li>
        </ul>
      </div>
    </main>
  );
}
