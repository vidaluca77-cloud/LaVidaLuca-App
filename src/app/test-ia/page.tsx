'use client';
import { useState } from 'react';

export default function TestIA() {
  const [question, setQuestion] = useState("Comment améliorer la fertilité d'un sol argileux ?");
  const [response, setResponse] = useState<any>(null);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError("");
    
    try {
      const res = await fetch(`${process.env.NEXT_PUBLIC_IA_API_URL}/guide`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ question })
      });
      
      if (!res.ok) {
        throw new Error(`Erreur ${res.status}`);
      }
      
      const data = await res.json();
      setResponse(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Erreur inconnue");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-4xl mx-auto p-6">
      <h1 className="text-2xl font-bold mb-6">Test de l'IA agricole</h1>
      
      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <label className="block mb-2">Question :</label>
          <textarea 
            value={question}
            onChange={(e) => setQuestion(e.target.value)}
            className="w-full p-2 border rounded"
            rows={3}
          />
        </div>
        
        <button 
          type="submit"
          disabled={loading}
          className={`px-4 py-2 rounded ${
            loading 
              ? 'bg-gray-400' 
              : 'bg-green-500 hover:bg-green-600'
          } text-white`}
        >
          {loading ? 'Chargement...' : 'Demander'}
        </button>
      </form>

      {error && (
        <div className="mt-4 p-4 bg-red-100 text-red-700 rounded">
          {error}
        </div>
      )}

      {response && (
        <div className="mt-6 space-y-4">
          <h2 className="font-semibold">Réponse :</h2>
          <pre className="whitespace-pre-wrap bg-gray-100 p-4 rounded">
            {JSON.stringify(response, null, 2)}
          </pre>
        </div>
      )}
    </div>
  );
}