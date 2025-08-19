// src/utils/matching.ts
import { UserProfile, Suggestion, Activity } from "@/types";
import { ACTIVITIES } from "./activities";

export const calculateMatching = (profile: UserProfile): Suggestion[] => {
  const suggestions = ACTIVITIES.map((activity) => {
    let score = 0;
    const reasons: string[] = [];

    // Compétences communes
    const commonSkills = activity.skill_tags.filter((skill) =>
      profile.skills.includes(skill)
    );
    if (commonSkills.length > 0) {
      score += commonSkills.length * 15;
      reasons.push(`Compétences correspondantes : ${commonSkills.join(", ")}`);
    }

    // Préférences de catégories
    if (profile.preferences.includes(activity.category)) {
      score += 25;
      const categoryNames = {
        agri: "Agriculture",
        transfo: "Transformation",
        artisanat: "Artisanat",
        nature: "Environnement",
        social: "Animation",
      };
      reasons.push(`Catégorie préférée : ${categoryNames[activity.category]}`);
    }

    // Durée adaptée
    if (activity.duration_min <= 90) {
      score += 10;
      reasons.push("Durée adaptée pour débuter");
    }

    // Sécurité
    if (activity.safety_level <= 2) {
      score += 10;
      if (activity.safety_level === 1) {
        reasons.push("Activité sans risque particulier");
      }
    }

    // Disponibilité (simulation)
    if (
      profile.availability.includes("weekend") ||
      profile.availability.includes("semaine")
    ) {
      score += 15;
      reasons.push("Compatible avec vos disponibilités");
    }

    return { activity, score, reasons };
  });

  return suggestions.sort((a, b) => b.score - a.score).slice(0, 3);
};
