"use client";
import React, { useState, useEffect } from "react";

interface User {
  id: number;
  email: string;
  first_name: string;
  last_name: string;
  created_at: string;
  is_active: boolean;
}

interface Activity {
  id: number;
  title: string;
  category: string;
  duration: number;
  description: string;
  created_at: string;
}

interface UserStats {
  totalActivities: number;
  recentActivities: Activity[];
  userSince: string;
}

export default function DashboardPage() {
  const [user, setUser] = useState<User | null>(null);
  const [stats, setStats] = useState<UserStats>({
    totalActivities: 0,
    recentActivities: [],
    userSince: "",
  });
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [isEditing, setIsEditing] = useState(false);
  const [editForm, setEditForm] = useState({
    first_name: "",
    last_name: "",
  });

  const apiUrl = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

  useEffect(() => {
    const token = localStorage.getItem("token");
    if (!token) {
      window.location.href = "/auth";
      return;
    }

    fetchUserData(token);
  }, []);

  const fetchUserData = async (token: string) => {
    try {
      setLoading(true);
      
      // Fetch user profile
      const userResponse = await fetch(`${apiUrl}/api/v1/users/me`, {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });

      if (!userResponse.ok) {
        if (userResponse.status === 401) {
          localStorage.removeItem("token");
          window.location.href = "/auth";
          return;
        }
        throw new Error("Failed to fetch user data");
      }

      const userData = await userResponse.json();
      setUser(userData.data);
      setEditForm({
        first_name: userData.data.first_name,
        last_name: userData.data.last_name,
      });

      // Fetch user activities
      const activitiesResponse = await fetch(`${apiUrl}/api/v1/activities?limit=5`, {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });

      if (activitiesResponse.ok) {
        const activitiesData = await activitiesResponse.json();
        setStats({
          totalActivities: activitiesData.data.total || 0,
          recentActivities: activitiesData.data.activities || [],
          userSince: userData.data.created_at,
        });
      }
    } catch (err) {
      setError("Erreur lors du chargement des données utilisateur");
      console.error("Error fetching user data:", err);
    } finally {
      setLoading(false);
    }
  };

  const handleUpdateProfile = async (e: React.FormEvent) => {
    e.preventDefault();
    const token = localStorage.getItem("token");
    if (!token) return;

    try {
      const response = await fetch(`${apiUrl}/api/v1/users/me`, {
        method: "PUT",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify(editForm),
      });

      if (response.ok) {
        const updatedUser = await response.json();
        setUser(updatedUser.data);
        setIsEditing(false);
      } else {
        setError("Erreur lors de la mise à jour du profil");
      }
    } catch (err) {
      setError("Erreur lors de la mise à jour du profil");
    }
  };

  const handleLogout = () => {
    localStorage.removeItem("token");
    window.location.href = "/";
  };

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString("fr-FR", {
      year: "numeric",
      month: "long",
      day: "numeric",
    });
  };

  if (loading) {
    return (
      <div className="min-h-screen gradient-bg flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin w-8 h-8 border-4 border-primary-600 border-t-transparent rounded-full mx-auto mb-4"></div>
          <p className="text-neutral-600">Chargement de votre tableau de bord...</p>
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
            <a href="/proposer-aide" className="text-neutral-700 hover:text-primary-600 transition-colors font-medium">
              Contribuer
            </a>
            <a href="/test-ia" className="text-neutral-700 hover:text-primary-600 transition-colors font-medium">
              Assistant IA
            </a>
            <span className="text-primary-600 font-medium border-b-2 border-primary-600">
              Dashboard
            </span>
            <button
              onClick={handleLogout}
              className="text-red-600 hover:text-red-700 transition-colors font-medium"
            >
              Déconnexion
            </button>
          </div>
        </div>
      </nav>

      <main className="container pb-20">
        {/* Header */}
        <section className="mb-12">
          <div className="card bg-gradient-to-r from-primary-50 to-green-50 border-primary-200">
            <div className="flex items-center justify-between">
              <div>
                <h1 className="text-gradient mb-2">
                  Bienvenue, {user?.first_name}!
                </h1>
                <p className="text-neutral-600">
                  Gérez votre profil et consultez vos activités
                </p>
              </div>
              <div className="text-6xl">🌱</div>
            </div>
          </div>
        </section>

        {/* Error Message */}
        {error && (
          <section className="mb-8">
            <div className="card bg-gradient-to-r from-red-50 to-red-100 border-red-200">
              <div className="flex items-center space-x-3">
                <div className="text-2xl">⚠️</div>
                <p className="text-red-700">{error}</p>
              </div>
            </div>
          </section>
        )}

        <div className="grid lg:grid-cols-3 gap-8">
          {/* Profile Section */}
          <div className="lg:col-span-2">
            <div className="card">
              <div className="flex items-center justify-between mb-6">
                <h2 className="font-display font-semibold text-2xl text-neutral-800">
                  Mon Profil
                </h2>
                <button
                  onClick={() => setIsEditing(!isEditing)}
                  className="btn btn-secondary"
                >
                  {isEditing ? "Annuler" : "Modifier"}
                </button>
              </div>

              {!isEditing ? (
                <div className="space-y-4">
                  <div className="grid md:grid-cols-2 gap-6">
                    <div>
                      <label className="block text-sm font-medium text-neutral-700 mb-1">
                        Prénom
                      </label>
                      <p className="text-lg text-neutral-800">{user?.first_name}</p>
                    </div>
                    <div>
                      <label className="block text-sm font-medium text-neutral-700 mb-1">
                        Nom
                      </label>
                      <p className="text-lg text-neutral-800">{user?.last_name}</p>
                    </div>
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-neutral-700 mb-1">
                      Email
                    </label>
                    <p className="text-lg text-neutral-800">{user?.email}</p>
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-neutral-700 mb-1">
                      Membre depuis
                    </label>
                    <p className="text-lg text-neutral-800">
                      {user?.created_at && formatDate(user.created_at)}
                    </p>
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-neutral-700 mb-1">
                      Statut
                    </label>
                    <span className={`inline-flex items-center px-3 py-1 rounded-full text-sm font-medium ${
                      user?.is_active
                        ? "bg-green-100 text-green-800"
                        : "bg-red-100 text-red-800"
                    }`}>
                      {user?.is_active ? "Actif" : "Inactif"}
                    </span>
                  </div>
                </div>
              ) : (
                <form onSubmit={handleUpdateProfile} className="space-y-4">
                  <div className="grid md:grid-cols-2 gap-6">
                    <div>
                      <label htmlFor="edit_first_name" className="block text-sm font-medium text-neutral-700 mb-1">
                        Prénom
                      </label>
                      <input
                        type="text"
                        id="edit_first_name"
                        value={editForm.first_name}
                        onChange={(e) => setEditForm({ ...editForm, first_name: e.target.value })}
                        className="w-full px-3 py-2 border border-neutral-200 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500 transition-colors"
                        required
                      />
                    </div>
                    <div>
                      <label htmlFor="edit_last_name" className="block text-sm font-medium text-neutral-700 mb-1">
                        Nom
                      </label>
                      <input
                        type="text"
                        id="edit_last_name"
                        value={editForm.last_name}
                        onChange={(e) => setEditForm({ ...editForm, last_name: e.target.value })}
                        className="w-full px-3 py-2 border border-neutral-200 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500 transition-colors"
                        required
                      />
                    </div>
                  </div>
                  <div className="flex gap-4">
                    <button type="submit" className="btn btn-primary">
                      Sauvegarder
                    </button>
                    <button
                      type="button"
                      onClick={() => setIsEditing(false)}
                      className="btn btn-secondary"
                    >
                      Annuler
                    </button>
                  </div>
                </form>
              )}
            </div>
          </div>

          {/* Stats Sidebar */}
          <div>
            <div className="card">
              <h3 className="font-display font-semibold text-xl mb-6 text-neutral-800">
                Mes Statistiques
              </h3>
              
              <div className="space-y-4">
                <div className="text-center p-4 bg-primary-50 rounded-lg border border-primary-200">
                  <div className="text-3xl font-bold text-primary-600 mb-1">
                    {stats.totalActivities}
                  </div>
                  <div className="text-sm text-primary-700">
                    Activités créées
                  </div>
                </div>

                <div className="text-center p-4 bg-green-50 rounded-lg border border-green-200">
                  <div className="text-3xl font-bold text-green-600 mb-1">
                    {stats.recentActivities.length}
                  </div>
                  <div className="text-sm text-green-700">
                    Activités récentes
                  </div>
                </div>
              </div>

              <div className="mt-6">
                <h4 className="font-medium text-neutral-800 mb-3">Actions rapides</h4>
                <div className="space-y-2">
                  <a href="/activites" className="block w-full btn btn-primary text-center">
                    📚 Voir les activités
                  </a>
                  <a href="/proposer-aide" className="block w-full btn btn-secondary text-center">
                    ➕ Créer une activité
                  </a>
                  <a href="/test-ia" className="block w-full btn btn-secondary text-center">
                    🤖 Assistant IA
                  </a>
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Recent Activities */}
        {stats.recentActivities.length > 0 && (
          <section className="mt-12">
            <div className="card">
              <h3 className="font-display font-semibold text-2xl mb-6 text-neutral-800">
                Activités récentes
              </h3>
              
              <div className="space-y-4">
                {stats.recentActivities.map((activity) => (
                  <div key={activity.id} className="p-4 border border-neutral-200 rounded-lg hover:bg-neutral-50 transition-colors">
                    <div className="flex items-start justify-between">
                      <div>
                        <h4 className="font-medium text-neutral-800 mb-1">
                          {activity.title}
                        </h4>
                        <p className="text-sm text-neutral-600 mb-2">
                          {activity.description}
                        </p>
                        <div className="flex items-center space-x-4 text-xs text-neutral-500">
                          <span>📁 {activity.category}</span>
                          <span>⏱️ {activity.duration} min</span>
                          <span>📅 {formatDate(activity.created_at)}</span>
                        </div>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </section>
        )}

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