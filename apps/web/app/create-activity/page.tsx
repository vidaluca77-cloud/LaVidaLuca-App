"use client";
import React, { useState, useEffect } from "react";

interface ActivityForm {
  title: string;
  description: string;
  category: "agri" | "transfo" | "artisanat" | "nature" | "social" | "";
  duration: number;
  safety_level: 1 | 2;
  materials_needed: string;
  learning_objectives: string;
}

const CATEGORIES = {
  agri: { label: "Agriculture", icon: "🌱", color: "from-green-100 to-green-200" },
  transfo: { label: "Transformation", icon: "🏭", color: "from-earth-100 to-earth-200" },
  artisanat: { label: "Artisanat", icon: "🔨", color: "from-neutral-100 to-neutral-200" },
  nature: { label: "Environnement", icon: "🌿", color: "from-green-50 to-earth-50" },
  social: { label: "Animation", icon: "👥", color: "from-primary-100 to-primary-200" },
};

export default function CreateActivityPage() {
  const [form, setForm] = useState<ActivityForm>({
    title: "",
    description: "",
    category: "",
    duration: 60,
    safety_level: 1,
    materials_needed: "",
    learning_objectives: "",
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");
  const [isLoggedIn, setIsLoggedIn] = useState(false);

  const apiUrl = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

  useEffect(() => {
    const token = localStorage.getItem("token");
    if (!token) {
      window.location.href = "/auth";
      return;
    }
    setIsLoggedIn(true);
  }, []);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    const token = localStorage.getItem("token");
    if (!token) {
      window.location.href = "/auth";
      return;
    }

    setLoading(true);
    setError("");

    try {
      const response = await fetch(`${apiUrl}/api/v1/activities`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify(form),
      });

      if (response.ok) {
        setSuccess("Activité créée avec succès!");
        setForm({
          title: "",
          description: "",
          category: "",
          duration: 60,
          safety_level: 1,
          materials_needed: "",
          learning_objectives: "",
        });
        setTimeout(() => {
          window.location.href = "/activites";
        }, 2000);
      } else {
        const data = await response.json();
        setError(data.detail || "Erreur lors de la création de l'activité");
      }
    } catch (err) {
      setError("Erreur de connexion. Veuillez réessayer.");
    } finally {
      setLoading(false);
    }
  };

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement>) => {
    const { name, value } = e.target;
    setForm(prev => ({
      ...prev,
      [name]: name === "duration" || name === "safety_level" ? Number(value) : value,
    }));
  };

  if (!isLoggedIn) {
    return (
      <div className="min-h-screen gradient-bg flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin w-8 h-8 border-4 border-primary-600 border-t-transparent rounded-full mx-auto mb-4"></div>
          <p className="text-neutral-600">Vérification de l'authentification...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen gradient-bg">
      {/* Navigation */}
      <nav className="container py-6">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-2">
            <div className="w-8 h-8 bg-gradient-to-br from-green-500 to-earth-500 rounded-lg"></div>
            <a href="/" className="text-xl font-display font-semibold text-gradient">
              La Vida Luca
            </a>
          </div>
          <div className="hidden md:flex items-center space-x-8">
            <a href="/activites" className="text-neutral-700 hover:text-primary-600 transition-colors font-medium">
              Activités
            </a>
            <a href="/dashboard" className="text-neutral-700 hover:text-primary-600 transition-colors font-medium">
              Dashboard
            </a>
            <a href="/test-ia" className="text-neutral-700 hover:text-primary-600 transition-colors font-medium">
              Assistant IA
            </a>
            <span className="text-primary-600 font-medium border-b-2 border-primary-600">
              Créer une activité
            </span>
          </div>
        </div>
      </nav>

      <main className="container pb-20">
        {/* Header */}
        <section className="text-center mb-12">
          <h1 className="text-gradient mb-4">
            Créer une nouvelle activité
          </h1>
          <p className="text-xl text-neutral-600 mb-2 max-w-3xl mx-auto">
            Partagez vos connaissances avec la communauté MFR
          </p>
          <p className="text-neutral-500 max-w-2xl mx-auto">
            Proposez une activité pédagogique pour enrichir le catalogue d'apprentissage
          </p>
        </section>

        {/* Messages */}
        {error && (
          <section className="mb-8">
            <div className="card max-w-4xl mx-auto bg-gradient-to-r from-red-50 to-red-100 border-red-200">
              <div className="flex items-center space-x-3">
                <div className="text-2xl">⚠️</div>
                <p className="text-red-700">{error}</p>
              </div>
            </div>
          </section>
        )}

        {success && (
          <section className="mb-8">
            <div className="card max-w-4xl mx-auto bg-gradient-to-r from-green-50 to-green-100 border-green-200">
              <div className="flex items-center space-x-3">
                <div className="text-2xl">✅</div>
                <p className="text-green-700">{success}</p>
              </div>
            </div>
          </section>
        )}

        {/* Form */}
        <section className="max-w-4xl mx-auto">
          <form onSubmit={handleSubmit} className="card">
            <div className="grid md:grid-cols-2 gap-8">
              {/* Left Column */}
              <div className="space-y-6">
                <h3 className="font-display font-semibold text-xl text-neutral-800 mb-4">
                  Informations générales
                </h3>

                <div>
                  <label htmlFor="title" className="block text-sm font-medium text-neutral-700 mb-2">
                    Titre de l'activité *
                  </label>
                  <input
                    type="text"
                    id="title"
                    name="title"
                    value={form.title}
                    onChange={handleChange}
                    className="w-full px-4 py-3 border border-neutral-200 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500 transition-colors"
                    placeholder="Ex: Culture de légumes bio en serre"
                    required
                  />
                </div>

                <div>
                  <label htmlFor="description" className="block text-sm font-medium text-neutral-700 mb-2">
                    Description *
                  </label>
                  <textarea
                    id="description"
                    name="description"
                    value={form.description}
                    onChange={handleChange}
                    rows={4}
                    className="w-full px-4 py-3 border border-neutral-200 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500 transition-colors resize-none"
                    placeholder="Décrivez l'activité, ses objectifs et son déroulement..."
                    required
                  />
                </div>

                <div>
                  <label htmlFor="category" className="block text-sm font-medium text-neutral-700 mb-2">
                    Catégorie *
                  </label>
                  <select
                    id="category"
                    name="category"
                    value={form.category}
                    onChange={handleChange}
                    className="w-full px-4 py-3 border border-neutral-200 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500 transition-colors"
                    required
                  >
                    <option value="">Sélectionner une catégorie</option>
                    {Object.entries(CATEGORIES).map(([key, cat]) => (
                      <option key={key} value={key}>
                        {cat.icon} {cat.label}
                      </option>
                    ))}
                  </select>
                </div>

                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <label htmlFor="duration" className="block text-sm font-medium text-neutral-700 mb-2">
                      Durée (minutes) *
                    </label>
                    <input
                      type="number"
                      id="duration"
                      name="duration"
                      value={form.duration}
                      onChange={handleChange}
                      min="15"
                      max="480"
                      className="w-full px-4 py-3 border border-neutral-200 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500 transition-colors"
                      required
                    />
                  </div>

                  <div>
                    <label htmlFor="safety_level" className="block text-sm font-medium text-neutral-700 mb-2">
                      Niveau de sécurité *
                    </label>
                    <select
                      id="safety_level"
                      name="safety_level"
                      value={form.safety_level}
                      onChange={handleChange}
                      className="w-full px-4 py-3 border border-neutral-200 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500 transition-colors"
                      required
                    >
                      <option value={1}>🟢 Niveau 1 - Standard</option>
                      <option value={2}>🟡 Niveau 2 - Renforcé</option>
                    </select>
                  </div>
                </div>
              </div>

              {/* Right Column */}
              <div className="space-y-6">
                <h3 className="font-display font-semibold text-xl text-neutral-800 mb-4">
                  Détails pédagogiques
                </h3>

                <div>
                  <label htmlFor="learning_objectives" className="block text-sm font-medium text-neutral-700 mb-2">
                    Objectifs d'apprentissage *
                  </label>
                  <textarea
                    id="learning_objectives"
                    name="learning_objectives"
                    value={form.learning_objectives}
                    onChange={handleChange}
                    rows={4}
                    className="w-full px-4 py-3 border border-neutral-200 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500 transition-colors resize-none"
                    placeholder="Quels sont les objectifs pédagogiques de cette activité?"
                    required
                  />
                </div>

                <div>
                  <label htmlFor="materials_needed" className="block text-sm font-medium text-neutral-700 mb-2">
                    Matériel nécessaire
                  </label>
                  <textarea
                    id="materials_needed"
                    name="materials_needed"
                    value={form.materials_needed}
                    onChange={handleChange}
                    rows={4}
                    className="w-full px-4 py-3 border border-neutral-200 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500 transition-colors resize-none"
                    placeholder="Listez le matériel et les ressources nécessaires..."
                  />
                </div>

                {/* Preview */}
                {form.category && (
                  <div className="p-4 bg-gradient-to-br border rounded-lg">
                    <h4 className="font-medium text-neutral-700 mb-2">Aperçu</h4>
                    <div className={`p-4 rounded-lg bg-gradient-to-br ${CATEGORIES[form.category as keyof typeof CATEGORIES].color}`}>
                      <div className="flex items-center justify-between mb-2">
                        <span className="text-2xl">{CATEGORIES[form.category as keyof typeof CATEGORIES].icon}</span>
                        <span className="text-xs px-2 py-1 bg-white/70 rounded-full">
                          {form.duration} min
                        </span>
                      </div>
                      <h5 className="font-medium text-neutral-800 mb-1">
                        {form.title || "Titre de l'activité"}
                      </h5>
                      <p className="text-sm text-neutral-600">
                        {form.description || "Description de l'activité"}
                      </p>
                    </div>
                  </div>
                )}
              </div>
            </div>

            {/* Submit Button */}
            <div className="mt-8 flex justify-center">
              <button
                type="submit"
                disabled={loading}
                className={`btn btn-primary text-lg px-12 py-4 ${loading ? "opacity-50 cursor-not-allowed" : ""}`}
              >
                {loading ? (
                  <>
                    <div className="animate-spin w-5 h-5 border-2 border-white border-t-transparent rounded-full mr-2"></div>
                    Création en cours...
                  </>
                ) : (
                  "🚀 Créer l'activité"
                )}
              </button>
            </div>
          </form>
        </section>

        {/* Back to Dashboard */}
        <section className="text-center mt-16">
          <a href="/dashboard" className="btn btn-secondary">
            ← Retour au dashboard
          </a>
        </section>
      </main>
    </div>
  );
}