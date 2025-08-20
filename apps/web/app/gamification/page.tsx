"use client";

import { useState, useEffect } from 'react';

interface UserStats {
  total_points: number;
  current_level: number;
  experience_points: number;
  xp_for_next_level: number;
  xp_progress: number;
  xp_needed: number;
  activities_completed: number;
  skills_learned: number;
  achievements_earned: number;
}

interface Skill {
  id: number;
  name: string;
  description: string;
  category: string;
}

interface Achievement {
  id: number;
  name: string;
  description: string;
  points_reward: number;
  category: string;
  icon?: string;
}

interface LeaderboardEntry {
  username: string;
  total_points: number;
  current_level: number;
}

interface ActivityRecommendation {
  activity_id: number;
  title: string;
  category: string;
  difficulty_level: string;
  points_reward: number;
  skills_taught: number[];
}

export default function GamificationDashboard() {
  const [userStats, setUserStats] = useState<UserStats | null>(null);
  const [skills, setSkills] = useState<Skill[]>([]);
  const [achievements, setAchievements] = useState<Achievement[]>([]);
  const [leaderboard, setLeaderboard] = useState<LeaderboardEntry[]>([]);
  const [recommendations, setRecommendations] = useState<ActivityRecommendation[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  // Mock data for demonstration (in a real app, this would come from API calls)
  useEffect(() => {
    // Simulate API loading delay
    setTimeout(() => {
      setUserStats({
        total_points: 165,
        current_level: 2,
        experience_points: 165,
        xp_for_next_level: 400,
        xp_progress: 65,
        xp_needed: 300,
        activities_completed: 3,
        skills_learned: 5,
        achievements_earned: 2
      });

      setSkills([
        { id: 1, name: "Jardinage Bio", description: "Techniques de jardinage biologique", category: "agriculture" },
        { id: 2, name: "Compostage", description: "Création et gestion de compost", category: "agriculture" },
        { id: 3, name: "Menuiserie", description: "Travail du bois", category: "artisanat" },
        { id: 4, name: "Communication", description: "Communication interpersonnelle", category: "social" },
        { id: 5, name: "Écologie", description: "Compréhension des écosystèmes", category: "nature" }
      ]);

      setAchievements([
        { id: 1, name: "Premier Pas", description: "Complétez votre première activité", points_reward: 25, category: "completion" },
        { id: 2, name: "Explorateur", description: "Complétez 5 activités", points_reward: 50, category: "completion" },
        { id: 3, name: "Centurion", description: "Accumulez 100 points", points_reward: 50, category: "points" }
      ]);

      setLeaderboard([
        { username: "Marie Dubois", total_points: 245, current_level: 3 },
        { username: "Jean Martin", total_points: 189, current_level: 2 },
        { username: "Sophie Bernard", total_points: 165, current_level: 2 },
        { username: "Pierre Leclerc", total_points: 134, current_level: 2 },
        { username: "Anne Petit", total_points: 98, current_level: 1 }
      ]);

      setRecommendations([
        { activity_id: 1, title: "Création d'un potager permaculture", category: "agriculture", difficulty_level: "intermediate", points_reward: 30, skills_taught: [1, 5] },
        { activity_id: 2, title: "Construction d'un abri à outils", category: "artisanat", difficulty_level: "beginner", points_reward: 20, skills_taught: [3] },
        { activity_id: 3, title: "Animation d'un atelier jeunesse", category: "social", difficulty_level: "advanced", points_reward: 40, skills_taught: [4] }
      ]);

      setLoading(false);
    }, 1000);
  }, []);

  const getProgressPercentage = () => {
    if (!userStats) return 0;
    return (userStats.xp_progress / (userStats.xp_progress + userStats.xp_needed)) * 100;
  };

  const getCategoryColor = (category: string) => {
    const colors: Record<string, string> = {
      agriculture: "#4ade80",
      artisanat: "#f59e0b",
      social: "#3b82f6",
      nature: "#10b981",
      completion: "#8b5cf6",
      points: "#f97316"
    };
    return colors[category] || "#6b7280";
  };

  if (loading) {
    return (
      <main style={{ padding: "32px", maxWidth: 1200, margin: "0 auto" }}>
        <div style={{ textAlign: "center", padding: "60px 0" }}>
          <div style={{ 
            width: 40, 
            height: 40, 
            border: "4px solid #f3f4f6", 
            borderTop: "4px solid #3b82f6", 
            borderRadius: "50%", 
            animation: "spin 1s linear infinite",
            margin: "0 auto 16px"
          }}></div>
          <p>Chargement de votre tableau de bord...</p>
        </div>
      </main>
    );
  }

  if (error) {
    return (
      <main style={{ padding: "32px", maxWidth: 1200, margin: "0 auto" }}>
        <div style={{ 
          padding: "16px", 
          backgroundColor: "#fee2e2", 
          border: "1px solid #fca5a5", 
          borderRadius: 8, 
          color: "#dc2626" 
        }}>
          Erreur: {error}
        </div>
      </main>
    );
  }

  return (
    <main style={{ padding: "32px", maxWidth: 1200, margin: "0 auto" }}>
      <style jsx>{`
        @keyframes spin {
          0% { transform: rotate(0deg); }
          100% { transform: rotate(360deg); }
        }
      `}</style>
      
      <header style={{ marginBottom: 32 }}>
        <h1 style={{ fontSize: 36, fontWeight: 800, marginBottom: 8, color: "#1f2937" }}>
          🎮 Tableau de Bord Gamification
        </h1>
        <p style={{ fontSize: 18, color: "#6b7280" }}>
          Suivez votre progression et découvrez de nouvelles activités
        </p>
      </header>

      {/* User Stats Section */}
      {userStats && (
        <section style={{ marginBottom: 40 }}>
          <div style={{ 
            display: "grid", 
            gridTemplateColumns: "repeat(auto-fit, minmax(250px, 1fr))", 
            gap: 20, 
            marginBottom: 24 
          }}>
            <div style={{ 
              padding: 24, 
              backgroundColor: "white", 
              borderRadius: 12, 
              boxShadow: "0 1px 3px rgba(0,0,0,0.1)",
              border: "1px solid #e5e7eb"
            }}>
              <h3 style={{ fontSize: 18, fontWeight: 600, marginBottom: 8, color: "#1f2937" }}>
                📊 Statistiques
              </h3>
              <div style={{ display: "grid", gridTemplateColumns: "repeat(2, 1fr)", gap: 12 }}>
                <div>
                  <p style={{ fontSize: 14, color: "#6b7280", margin: 0 }}>Points Total</p>
                  <p style={{ fontSize: 24, fontWeight: 700, color: "#3b82f6", margin: 0 }}>
                    {userStats.total_points}
                  </p>
                </div>
                <div>
                  <p style={{ fontSize: 14, color: "#6b7280", margin: 0 }}>Niveau</p>
                  <p style={{ fontSize: 24, fontWeight: 700, color: "#10b981", margin: 0 }}>
                    {userStats.current_level}
                  </p>
                </div>
                <div>
                  <p style={{ fontSize: 14, color: "#6b7280", margin: 0 }}>Activités</p>
                  <p style={{ fontSize: 24, fontWeight: 700, color: "#f59e0b", margin: 0 }}>
                    {userStats.activities_completed}
                  </p>
                </div>
                <div>
                  <p style={{ fontSize: 14, color: "#6b7280", margin: 0 }}>Compétences</p>
                  <p style={{ fontSize: 24, fontWeight: 700, color: "#8b5cf6", margin: 0 }}>
                    {userStats.skills_learned}
                  </p>
                </div>
              </div>
            </div>

            <div style={{ 
              padding: 24, 
              backgroundColor: "white", 
              borderRadius: 12, 
              boxShadow: "0 1px 3px rgba(0,0,0,0.1)",
              border: "1px solid #e5e7eb"
            }}>
              <h3 style={{ fontSize: 18, fontWeight: 600, marginBottom: 16, color: "#1f2937" }}>
                🎯 Progression vers le niveau {userStats.current_level + 1}
              </h3>
              <div style={{ marginBottom: 8 }}>
                <div style={{
                  width: "100%",
                  height: 8,
                  backgroundColor: "#e5e7eb",
                  borderRadius: 4,
                  overflow: "hidden"
                }}>
                  <div style={{
                    width: `${getProgressPercentage()}%`,
                    height: "100%",
                    backgroundColor: "#3b82f6",
                    transition: "width 0.3s ease"
                  }}></div>
                </div>
              </div>
              <p style={{ fontSize: 14, color: "#6b7280", margin: 0 }}>
                {userStats.xp_progress} / {userStats.xp_progress + userStats.xp_needed} XP
              </p>
              <p style={{ fontSize: 12, color: "#9ca3af", margin: "4px 0 0 0" }}>
                {userStats.xp_needed} XP restants
              </p>
            </div>
          </div>
        </section>
      )}

      {/* Skills and Achievements Grid */}
      <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 32, marginBottom: 40 }}>
        {/* Skills Section */}
        <section>
          <h2 style={{ fontSize: 24, fontWeight: 700, marginBottom: 16, color: "#1f2937" }}>
            🎓 Mes Compétences
          </h2>
          <div style={{ display: "grid", gap: 12 }}>
            {skills.map((skill) => (
              <div key={skill.id} style={{
                padding: 16,
                backgroundColor: "white",
                borderRadius: 8,
                border: "1px solid #e5e7eb",
                borderLeft: `4px solid ${getCategoryColor(skill.category)}`
              }}>
                <h4 style={{ fontSize: 16, fontWeight: 600, margin: "0 0 4px 0", color: "#1f2937" }}>
                  {skill.name}
                </h4>
                <p style={{ fontSize: 14, color: "#6b7280", margin: "0 0 8px 0" }}>
                  {skill.description}
                </p>
                <span style={{
                  display: "inline-block",
                  padding: "2px 8px",
                  backgroundColor: getCategoryColor(skill.category),
                  color: "white",
                  borderRadius: 12,
                  fontSize: 12,
                  fontWeight: 500
                }}>
                  {skill.category}
                </span>
              </div>
            ))}
          </div>
        </section>

        {/* Achievements Section */}
        <section>
          <h2 style={{ fontSize: 24, fontWeight: 700, marginBottom: 16, color: "#1f2937" }}>
            🏆 Mes Réussites
          </h2>
          <div style={{ display: "grid", gap: 12 }}>
            {achievements.map((achievement) => (
              <div key={achievement.id} style={{
                padding: 16,
                backgroundColor: "white",
                borderRadius: 8,
                border: "1px solid #e5e7eb",
                borderLeft: `4px solid ${getCategoryColor(achievement.category)}`
              }}>
                <div style={{ display: "flex", justifyContent: "space-between", alignItems: "flex-start" }}>
                  <div style={{ flex: 1 }}>
                    <h4 style={{ fontSize: 16, fontWeight: 600, margin: "0 0 4px 0", color: "#1f2937" }}>
                      {achievement.name}
                    </h4>
                    <p style={{ fontSize: 14, color: "#6b7280", margin: "0 0 8px 0" }}>
                      {achievement.description}
                    </p>
                  </div>
                  <span style={{
                    padding: "4px 8px",
                    backgroundColor: "#f59e0b",
                    color: "white",
                    borderRadius: 8,
                    fontSize: 12,
                    fontWeight: 600
                  }}>
                    +{achievement.points_reward} pts
                  </span>
                </div>
              </div>
            ))}
          </div>
        </section>
      </div>

      {/* Leaderboard and Recommendations */}
      <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 32 }}>
        {/* Leaderboard */}
        <section>
          <h2 style={{ fontSize: 24, fontWeight: 700, marginBottom: 16, color: "#1f2937" }}>
            🏅 Classement
          </h2>
          <div style={{
            backgroundColor: "white",
            borderRadius: 12,
            overflow: "hidden",
            border: "1px solid #e5e7eb"
          }}>
            {leaderboard.map((entry, index) => (
              <div key={entry.username} style={{
                padding: 16,
                borderBottom: index < leaderboard.length - 1 ? "1px solid #e5e7eb" : "none",
                display: "flex",
                alignItems: "center",
                justifyContent: "space-between"
              }}>
                <div style={{ display: "flex", alignItems: "center", gap: 12 }}>
                  <span style={{
                    display: "flex",
                    alignItems: "center",
                    justifyContent: "center",
                    width: 32,
                    height: 32,
                    borderRadius: "50%",
                    backgroundColor: index === 0 ? "#fbbf24" : index === 1 ? "#d1d5db" : index === 2 ? "#f97316" : "#e5e7eb",
                    color: index < 3 ? "white" : "#6b7280",
                    fontSize: 14,
                    fontWeight: 600
                  }}>
                    {index + 1}
                  </span>
                  <span style={{ fontSize: 16, fontWeight: 500, color: "#1f2937" }}>
                    {entry.username}
                  </span>
                </div>
                <div style={{ textAlign: "right" }}>
                  <div style={{ fontSize: 16, fontWeight: 600, color: "#3b82f6" }}>
                    {entry.total_points} pts
                  </div>
                  <div style={{ fontSize: 12, color: "#6b7280" }}>
                    Niveau {entry.current_level}
                  </div>
                </div>
              </div>
            ))}
          </div>
        </section>

        {/* Recommendations */}
        <section>
          <h2 style={{ fontSize: 24, fontWeight: 700, marginBottom: 16, color: "#1f2937" }}>
            💡 Activités Recommandées
          </h2>
          <div style={{ display: "grid", gap: 12 }}>
            {recommendations.map((rec) => (
              <div key={rec.activity_id} style={{
                padding: 16,
                backgroundColor: "white",
                borderRadius: 8,
                border: "1px solid #e5e7eb",
                cursor: "pointer",
                transition: "all 0.2s ease"
              }}
              onMouseEnter={(e) => {
                e.currentTarget.style.transform = "translateY(-2px)";
                e.currentTarget.style.boxShadow = "0 4px 12px rgba(0,0,0,0.1)";
              }}
              onMouseLeave={(e) => {
                e.currentTarget.style.transform = "translateY(0)";
                e.currentTarget.style.boxShadow = "none";
              }}>
                <div style={{ display: "flex", justifyContent: "space-between", alignItems: "flex-start", marginBottom: 8 }}>
                  <h4 style={{ fontSize: 16, fontWeight: 600, margin: 0, color: "#1f2937" }}>
                    {rec.title}
                  </h4>
                  <span style={{
                    padding: "2px 6px",
                    backgroundColor: "#10b981",
                    color: "white",
                    borderRadius: 4,
                    fontSize: 12,
                    fontWeight: 500
                  }}>
                    +{rec.points_reward} pts
                  </span>
                </div>
                <div style={{ display: "flex", gap: 8, alignItems: "center" }}>
                  <span style={{
                    padding: "1px 6px",
                    backgroundColor: getCategoryColor(rec.category),
                    color: "white",
                    borderRadius: 8,
                    fontSize: 11,
                    fontWeight: 500
                  }}>
                    {rec.category}
                  </span>
                  <span style={{
                    padding: "1px 6px",
                    backgroundColor: "#6b7280",
                    color: "white",
                    borderRadius: 8,
                    fontSize: 11,
                    fontWeight: 500
                  }}>
                    {rec.difficulty_level}
                  </span>
                </div>
              </div>
            ))}
          </div>
        </section>
      </div>

      {/* Navigation Back */}
      <div style={{ marginTop: 40, textAlign: "center" }}>
        <a
          href="/"
          style={{
            display: "inline-block",
            padding: "12px 24px",
            backgroundColor: "#3b82f6",
            color: "white",
            textDecoration: "none",
            borderRadius: 8,
            fontWeight: 500,
            transition: "background-color 0.2s ease"
          }}
          onMouseEnter={(e) => e.currentTarget.style.backgroundColor = "#2563eb"}
          onMouseLeave={(e) => e.currentTarget.style.backgroundColor = "#3b82f6"}
        >
          ← Retour à l'accueil
        </a>
      </div>
    </main>
  );
}