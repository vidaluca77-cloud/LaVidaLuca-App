"use client";
import { useState } from "react";

export default function TestIA() {
  const [question, setQuestion] = useState("Comment améliorer la fertilité d'un sol argileux ?");
  const [loading, setLoading] = useState(false);
  const [response, setResponse] = useState(null);
  const [error, setError] = useState("");

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError("");
    
    try {
      const res = await fetch(`${process.env.NEXT_PUBLIC_IA_API_URL}/guide`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ question })
      });
      
      if (!res.ok) throw new Error("Erreur API");
      const data = await res.json();
      setResponse(data);
    } catch (err: any) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-4xl mx-auto p-6">
      <h1 className="text-2xl font-bold mb-6">Test de l'IA agricole</h1>
      
      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <label className="block text-sm font-medium mb-2">
            Votre question
          </label>
          <textarea
            value={question}
            onChange={(e) => setQuestion(e.target.value)}
            className="w-full h-32 p-3 border rounded"
            required
          />
        </div>
        
        <button
          type="submit"
          disabled={loading}
          className="px-4 py-2 bg-green-500 text-white rounded disabled:opacity-50"
        >
          {loading ? "Chargement..." : "Demander"}
        </button>
      </form>

      {error && (
        <div className="mt-6 p-4 bg-red-50 text-red-700 rounded">
          {error}
        </div>
      )}

      {response && (
        <div className="mt-6 space-y-4">
          <h2 className="text-xl font-semibold">{(response as any).title}</h2>
          
          <div className="p-4 bg-gray-50 rounded">
            <pre className="whitespace-pre-wrap">
              {JSON.stringify(response, null, 2)}
            </pre>
          </div>
        </div>
      )}
    </div>
  );
}