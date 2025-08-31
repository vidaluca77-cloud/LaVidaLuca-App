"use client";
import React, { useState } from "react";

export default function TestIA() {
  const [question, setQuestion] = useState("Comment améliorer un sol argileux compact ?");
  const [response, setResponse] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const api = process.env.NEXT_PUBLIC_API_URL || "http://127.0.0.1:8000";

  const exampleQuestions = [
    "Comment améliorer un sol argileux compact ?",
    "Quelles plantes pour débuter un potager ?",
    "Comment faire du compost rapidement ?",
    "Techniques de permaculture pour petit jardin",
    "Rotation des cultures en maraîchage bio",
    "Associations de légumes bénéfiques"
  ];

  async function askQuestion(e: React.FormEvent) {
    e.preventDefault();
    if (!question.trim()) return;

    setLoading(true);
    setError("");
    setResponse("");

    try {
      const res = await fetch(`${api}/api/v1/guide`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          question: question.trim(),
        }),
      });

      if (!res.ok) {
        throw new Error(`Erreur ${res.status}: ${res.statusText}`);
      }

      const data = await res.json();
      setResponse(data.response || data.answer || "Pas de réponse disponible");
    } catch (err) {
      console.error("Erreur API:", err);
      setError("Service temporairement indisponible. Veuillez réessayer plus tard.");
      setResponse("Le service d'IA n'est pas disponible en ce moment. Ceci est une démonstration de l'interface utilisateur.");
    } finally {
      setLoading(false);
    }
  }

  const handleExampleClick = (exampleQuestion: string) => {
    setQuestion(exampleQuestion);
  };

  return (
    <div className="min-h-screen gradient-bg">
      {/* Navigation */}
      <nav className="container py-6">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-2">
            <div className="w-8 h-8 bg-gradient-to-br from-green-500 to-earth-500 rounded-lg"></div>
            <a href="/" className="text-xl font-display font-semibold text-gradient">La Vida Luca</a>
          </div>
          <div className="hidden md:flex items-center space-x-8">
            <a href="/activites" className="text-neutral-700 hover:text-primary-600 transition-colors font-medium">
              Activités
            </a>
            <a href="/proposer-aide" className="text-neutral-700 hover:text-primary-600 transition-colors font-medium">
              Contribuer
            </a>
            <span className="text-primary-600 font-medium border-b-2 border-primary-600">
              Assistant IA
            </span>
          </div>
        </div>
      </nav>

      <main className="container pb-20">
        {/* Header */}
        <section className="text-center mb-12">
          <h1 className="text-gradient mb-4">
            Assistant IA Jardinage
          </h1>
          <p className="text-xl text-neutral-600 mb-2 max-w-3xl mx-auto">
            Obtenez des conseils personnalisés pour vos projets agricoles
          </p>
          <p className="text-neutral-500 max-w-2xl mx-auto">
            Notre assistant IA spécialisé en jardinage et permaculture répond à vos questions.
          </p>
          
          {/* API Status */}
          <div className="max-w-md mx-auto mt-6">
            <div className="card bg-gradient-to-r from-primary-50 to-primary-100 border-primary-200">
              <div className="flex items-center justify-center space-x-2 text-sm">
                <div className="w-2 h-2 bg-primary-500 rounded-full animate-pulse"></div>
                <span className="text-primary-700 font-medium">API: {api}</span>
              </div>
            </div>
          </div>
        </section>

        {/* Question Form */}
        <section className="max-w-4xl mx-auto mb-8">
          <form onSubmit={askQuestion} className="card">
            <h2 className="font-display font-semibold text-2xl mb-6 text-neutral-800">
              🤖 Posez votre question
            </h2>

            <div className="mb-6">
              <label htmlFor="question" className="block text-sm font-medium text-neutral-700 mb-3">
                Votre question sur le jardinage, la permaculture ou l'agriculture
              </label>
              <textarea
                id="question"
                value={question}
                onChange={(e) => setQuestion(e.target.value)}
                rows={4}
                className="w-full px-4 py-3 border border-neutral-200 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500 transition-colors resize-none"
                placeholder="Posez votre question ici..."
                required
              />
            </div>

            <div className="flex justify-center">
              <button
                type="submit"
                disabled={loading || !question.trim()}
                className={`btn btn-primary text-base px-8 py-3 ${
                  loading || !question.trim() ? 'opacity-50 cursor-not-allowed' : ''
                }`}
              >
                {loading ? (
                  <>
                    <div className="animate-spin w-4 h-4 border-2 border-white border-t-transparent rounded-full mr-2"></div>
                    Analyse en cours...
                  </>
                ) : (
                  '🚀 Poser la question'
                )}
              </button>
            </div>
          </form>
        </section>

        {/* Error Message */}
        {error && (
          <section className="max-w-4xl mx-auto mb-8">
            <div className="card bg-gradient-to-r from-red-50 to-red-100 border-red-200">
              <div className="flex items-center space-x-3">
                <div className="text-2xl">⚠️</div>
                <div>
                  <h3 className="font-display font-semibold text-red-800 mb-1">
                    Erreur de connexion
                  </h3>
                  <p className="text-red-700">{error}</p>
                </div>
              </div>
            </div>
          </section>
        )}

        {/* Response */}
        {response && (
          <section className="max-w-4xl mx-auto mb-8">
            <div className="card bg-gradient-to-r from-green-50 to-green-100 border-green-200">
              <h3 className="font-display font-semibold text-lg mb-4 text-green-800 flex items-center">
                <span className="text-2xl mr-2">🌱</span>
                Réponse de l'assistant
              </h3>
              <div className="bg-white/60 rounded-lg p-4 border border-green-200">
                <pre className="whitespace-pre-wrap text-neutral-700 font-sans leading-relaxed">
                  {response}
                </pre>
              </div>
            </div>
          </section>
        )}

        {/* Example Questions */}
        <section className="max-w-4xl mx-auto">
          <div className="card">
            <h3 className="font-display font-semibold text-xl mb-6 text-neutral-800 flex items-center">
              <span className="text-2xl mr-2">💡</span>
              Questions d'exemple
            </h3>
            
            <div className="grid md:grid-cols-2 gap-4">
              {exampleQuestions.map((exampleQ, index) => (
                <button
                  key={index}
                  onClick={() => handleExampleClick(exampleQ)}
                  className="text-left p-4 border border-neutral-200 rounded-lg hover:bg-neutral-50 hover:border-primary-300 transition-all group"
                >
                  <div className="flex items-start space-x-3">
                    <span className="text-primary-500 group-hover:text-primary-600 transition-colors">
                      ❓
                    </span>
                    <span className="text-neutral-700 group-hover:text-neutral-800 transition-colors">
                      {exampleQ}
                    </span>
                  </div>
                </button>
              ))}
            </div>

            <div className="mt-6 p-4 bg-neutral-50 rounded-lg border border-neutral-200">
              <p className="text-sm text-neutral-600 leading-relaxed">
                <strong>💡 Conseil :</strong> Soyez spécifique dans vos questions pour obtenir des réponses plus précises. 
                Mentionnez votre région, le type de sol, la saison, etc.
              </p>
            </div>
          </div>
        </section>

        {/* Back to Home */}
        <section className="text-center mt-16">
          <a href="/" className="btn btn-secondary">
            ← Retour à l'accueil
          </a>
        </section>
      </main>
    </div>
  );
}