"use client";
import React, { useState } from "react";

type AuthMode = "login" | "register";

interface LoginForm {
  email: string;
  password: string;
}

interface RegisterForm {
  email: string;
  password: string;
  confirmPassword: string;
  first_name: string;
  last_name: string;
}

export default function AuthPage() {
  const [mode, setMode] = useState<AuthMode>("login");
  const [loginForm, setLoginForm] = useState<LoginForm>({
    email: "",
    password: "",
  });
  const [registerForm, setRegisterForm] = useState<RegisterForm>({
    email: "",
    password: "",
    confirmPassword: "",
    first_name: "",
    last_name: "",
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");

  const apiUrl = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError("");

    try {
      const response = await fetch(`${apiUrl}/api/v1/auth/login`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(loginForm),
      });

      const data = await response.json();

      if (response.ok) {
        setSuccess("Connexion réussie!");
        // Store the token (you might want to use a proper state management solution)
        localStorage.setItem("token", data.data.access_token);
        // Redirect to dashboard or home page
        window.location.href = "/dashboard";
      } else {
        setError(data.detail || "Erreur de connexion");
      }
    } catch (err) {
      setError("Erreur de connexion. Veuillez réessayer.");
    } finally {
      setLoading(false);
    }
  };

  const handleRegister = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError("");

    if (registerForm.password !== registerForm.confirmPassword) {
      setError("Les mots de passe ne correspondent pas");
      setLoading(false);
      return;
    }

    try {
      const response = await fetch(`${apiUrl}/api/v1/auth/register`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          email: registerForm.email,
          password: registerForm.password,
          first_name: registerForm.first_name,
          last_name: registerForm.last_name,
        }),
      });

      const data = await response.json();

      if (response.ok) {
        setSuccess("Inscription réussie! Vous pouvez maintenant vous connecter.");
        setMode("login");
        setRegisterForm({
          email: "",
          password: "",
          confirmPassword: "",
          first_name: "",
          last_name: "",
        });
      } else {
        setError(data.detail || "Erreur d'inscription");
      }
    } catch (err) {
      setError("Erreur d'inscription. Veuillez réessayer.");
    } finally {
      setLoading(false);
    }
  };

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
            <a href="/proposer-aide" className="text-neutral-700 hover:text-primary-600 transition-colors font-medium">
              Contribuer
            </a>
            <a href="/test-ia" className="text-neutral-700 hover:text-primary-600 transition-colors font-medium">
              Assistant IA
            </a>
          </div>
        </div>
      </nav>

      <main className="container pb-20">
        {/* Header */}
        <section className="text-center mb-12">
          <h1 className="text-gradient mb-4">
            {mode === "login" ? "Connexion" : "Inscription"}
          </h1>
          <p className="text-xl text-neutral-600 mb-2 max-w-3xl mx-auto">
            {mode === "login"
              ? "Connectez-vous à votre compte La Vida Luca"
              : "Rejoignez la communauté La Vida Luca"}
          </p>
        </section>

        {/* Auth Form */}
        <section className="max-w-md mx-auto">
          <div className="card">
            {/* Mode Toggle */}
            <div className="flex mb-6 bg-neutral-100 rounded-lg p-1">
              <button
                onClick={() => setMode("login")}
                className={`flex-1 py-2 px-4 rounded-md font-medium transition-all ${
                  mode === "login"
                    ? "bg-white text-primary-600 shadow-sm"
                    : "text-neutral-600 hover:text-neutral-800"
                }`}
              >
                Connexion
              </button>
              <button
                onClick={() => setMode("register")}
                className={`flex-1 py-2 px-4 rounded-md font-medium transition-all ${
                  mode === "register"
                    ? "bg-white text-primary-600 shadow-sm"
                    : "text-neutral-600 hover:text-neutral-800"
                }`}
              >
                Inscription
              </button>
            </div>

            {/* Error/Success Messages */}
            {error && (
              <div className="mb-4 p-3 bg-red-50 border border-red-200 text-red-700 rounded-lg text-sm">
                {error}
              </div>
            )}
            {success && (
              <div className="mb-4 p-3 bg-green-50 border border-green-200 text-green-700 rounded-lg text-sm">
                {success}
              </div>
            )}

            {/* Login Form */}
            {mode === "login" && (
              <form onSubmit={handleLogin} className="space-y-4">
                <div>
                  <label htmlFor="email" className="block text-sm font-medium text-neutral-700 mb-1">
                    Email
                  </label>
                  <input
                    type="email"
                    id="email"
                    value={loginForm.email}
                    onChange={(e) => setLoginForm({ ...loginForm, email: e.target.value })}
                    className="w-full px-3 py-2 border border-neutral-200 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500 transition-colors"
                    required
                  />
                </div>
                <div>
                  <label htmlFor="password" className="block text-sm font-medium text-neutral-700 mb-1">
                    Mot de passe
                  </label>
                  <input
                    type="password"
                    id="password"
                    value={loginForm.password}
                    onChange={(e) => setLoginForm({ ...loginForm, password: e.target.value })}
                    className="w-full px-3 py-2 border border-neutral-200 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500 transition-colors"
                    required
                  />
                </div>
                <button
                  type="submit"
                  disabled={loading}
                  className={`w-full btn btn-primary ${loading ? "opacity-50 cursor-not-allowed" : ""}`}
                >
                  {loading ? "Connexion..." : "Se connecter"}
                </button>
              </form>
            )}

            {/* Register Form */}
            {mode === "register" && (
              <form onSubmit={handleRegister} className="space-y-4">
                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <label htmlFor="first_name" className="block text-sm font-medium text-neutral-700 mb-1">
                      Prénom
                    </label>
                    <input
                      type="text"
                      id="first_name"
                      value={registerForm.first_name}
                      onChange={(e) => setRegisterForm({ ...registerForm, first_name: e.target.value })}
                      className="w-full px-3 py-2 border border-neutral-200 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500 transition-colors"
                      required
                    />
                  </div>
                  <div>
                    <label htmlFor="last_name" className="block text-sm font-medium text-neutral-700 mb-1">
                      Nom
                    </label>
                    <input
                      type="text"
                      id="last_name"
                      value={registerForm.last_name}
                      onChange={(e) => setRegisterForm({ ...registerForm, last_name: e.target.value })}
                      className="w-full px-3 py-2 border border-neutral-200 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500 transition-colors"
                      required
                    />
                  </div>
                </div>
                <div>
                  <label htmlFor="reg_email" className="block text-sm font-medium text-neutral-700 mb-1">
                    Email
                  </label>
                  <input
                    type="email"
                    id="reg_email"
                    value={registerForm.email}
                    onChange={(e) => setRegisterForm({ ...registerForm, email: e.target.value })}
                    className="w-full px-3 py-2 border border-neutral-200 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500 transition-colors"
                    required
                  />
                </div>
                <div>
                  <label htmlFor="reg_password" className="block text-sm font-medium text-neutral-700 mb-1">
                    Mot de passe
                  </label>
                  <input
                    type="password"
                    id="reg_password"
                    value={registerForm.password}
                    onChange={(e) => setRegisterForm({ ...registerForm, password: e.target.value })}
                    className="w-full px-3 py-2 border border-neutral-200 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500 transition-colors"
                    required
                  />
                </div>
                <div>
                  <label htmlFor="confirm_password" className="block text-sm font-medium text-neutral-700 mb-1">
                    Confirmer le mot de passe
                  </label>
                  <input
                    type="password"
                    id="confirm_password"
                    value={registerForm.confirmPassword}
                    onChange={(e) => setRegisterForm({ ...registerForm, confirmPassword: e.target.value })}
                    className="w-full px-3 py-2 border border-neutral-200 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500 transition-colors"
                    required
                  />
                </div>
                <button
                  type="submit"
                  disabled={loading}
                  className={`w-full btn btn-primary ${loading ? "opacity-50 cursor-not-allowed" : ""}`}
                >
                  {loading ? "Inscription..." : "S'inscrire"}
                </button>
              </form>
            )}

            {/* Additional Links */}
            <div className="mt-6 text-center">
              <p className="text-sm text-neutral-600">
                {mode === "login" ? "Pas encore de compte?" : "Déjà un compte?"}
                <button
                  onClick={() => setMode(mode === "login" ? "register" : "login")}
                  className="ml-1 text-primary-600 hover:text-primary-700 font-medium"
                >
                  {mode === "login" ? "S'inscrire" : "Se connecter"}
                </button>
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