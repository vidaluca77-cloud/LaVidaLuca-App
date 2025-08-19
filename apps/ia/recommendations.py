import openai
from typing import List, Dict, Any
from sqlalchemy.orm import Session
from models import Activity, User, UserProfile, user_skills, user_preferences, Recommendation
from config import settings

# Configuration OpenAI
openai.api_key = settings.OPENAI_API_KEY

class RecommendationEngine:
    def __init__(self, db: Session):
        self.db = db
    
    def calculate_matching_score(self, user_profile: UserProfile, activity: Activity, user_skills_list: List[str], user_preferences: List[str]) -> Dict[str, Any]:
        """Calculer le score de matching entre un profil utilisateur et une activité"""
        score = 0
        reasons = []
        
        # Compétences communes
        if activity.skill_tags and user_skills_list:
            common_skills = set(activity.skill_tags) & set(user_skills_list)
            if common_skills:
                score += len(common_skills) * 15
                reasons.append(f"Compétences correspondantes : {', '.join(common_skills)}")
        
        # Préférences de catégories
        if activity.category in user_preferences:
            score += 25
            category_names = {
                'agri': 'Agriculture',
                'transfo': 'Transformation', 
                'artisanat': 'Artisanat',
                'nature': 'Environnement',
                'social': 'Animation'
            }
            reasons.append(f"Catégorie préférée : {category_names.get(activity.category, activity.category)}")
        
        # Durée adaptée selon le niveau d'expérience
        if user_profile.experience_level == "debutant" and activity.duration_min <= 90:
            score += 10
            reasons.append('Durée adaptée pour débuter')
        elif user_profile.experience_level == "intermediaire" and 60 <= activity.duration_min <= 120:
            score += 10
            reasons.append('Durée adaptée à votre niveau')
        elif user_profile.experience_level == "avance":
            score += 5
            reasons.append('Activité accessible')
        
        # Sécurité selon le niveau d'expérience
        if user_profile.experience_level == "debutant" and activity.safety_level <= 1:
            score += 15
            reasons.append('Activité sans risque particulier')
        elif user_profile.experience_level == "intermediaire" and activity.safety_level <= 2:
            score += 10
            reasons.append('Niveau de sécurité adapté')
        elif user_profile.experience_level == "avance":
            score += 5
        
        # Disponibilité (simulation basée sur les créneaux)
        if user_profile.availability and any(av in ['weekend', 'semaine'] for av in user_profile.availability):
            score += 15
            reasons.append('Compatible avec vos disponibilités')
        
        return {
            'score': score,
            'reasons': reasons
        }
    
    async def generate_ai_explanation(self, user_profile: UserProfile, activity: Activity, score: float, reasons: List[str]) -> str:
        """Générer une explication IA personnalisée pour la recommandation"""
        if not settings.OPENAI_API_KEY:
            return f"Activité recommandée avec un score de {score}%. " + " ".join(reasons)
        
        try:
            prompt = f"""
            Tu es un conseiller pédagogique spécialisé dans l'agriculture et l'artisanat pour jeunes en MFR.
            
            Profil utilisateur:
            - Niveau d'expérience: {user_profile.experience_level}
            - Localisation: {user_profile.location or 'Non spécifiée'}
            - Disponibilités: {', '.join(user_profile.availability) if user_profile.availability else 'Non spécifiées'}
            
            Activité recommandée:
            - Titre: {activity.title}
            - Catégorie: {activity.category}
            - Durée: {activity.duration_min} minutes
            - Niveau de sécurité: {activity.safety_level}/3
            - Résumé: {activity.summary}
            
            Score de compatibilité: {score}%
            Raisons principales: {', '.join(reasons)}
            
            Rédige une explication personnalisée en 2-3 phrases qui explique pourquoi cette activité est recommandée pour ce profil utilisateur. Sois encourageant et pédagogique.
            """
            
            response = await openai.ChatCompletion.acreate(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=150,
                temperature=0.7
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            # Fallback en cas d'erreur OpenAI
            return f"Cette activité correspond bien à votre profil ({score}% de compatibilité). " + " ".join(reasons[:2])
    
    async def get_recommendations(self, user: User, limit: int = 10) -> List[Dict[str, Any]]:
        """Obtenir les recommandations pour un utilisateur"""
        # Charger le profil utilisateur
        profile = self.db.query(UserProfile).filter(UserProfile.user_id == user.id).first()
        if not profile:
            return []
        
        # Charger les compétences et préférences
        skills_result = self.db.execute(
            user_skills.select().where(user_skills.c.user_id == user.id)
        ).fetchall()
        user_skills_list = [row.skill_name for row in skills_result]
        
        prefs_result = self.db.execute(
            user_preferences.select().where(user_preferences.c.user_id == user.id)
        ).fetchall()
        user_prefs = [row.category for row in prefs_result]
        
        # Obtenir toutes les activités actives
        activities = self.db.query(Activity).filter(Activity.is_active == True).all()
        
        recommendations = []
        for activity in activities:
            matching = self.calculate_matching_score(profile, activity, user_skills_list, user_prefs)
            
            if matching['score'] > 0:  # Seulement les activités avec un score positif
                ai_explanation = await self.generate_ai_explanation(
                    profile, activity, matching['score'], matching['reasons']
                )
                
                recommendations.append({
                    'activity': activity,
                    'score': matching['score'],
                    'reasons': matching['reasons'],
                    'ai_explanation': ai_explanation
                })
        
        # Trier par score décroissant et limiter
        recommendations.sort(key=lambda x: x['score'], reverse=True)
        return recommendations[:limit]
    
    async def save_recommendations(self, user: User, recommendations: List[Dict[str, Any]]):
        """Sauvegarder les recommandations en base de données"""
        # Supprimer les anciennes recommandations
        self.db.query(Recommendation).filter(Recommendation.user_id == user.id).delete()
        
        # Sauvegarder les nouvelles recommandations
        for rec_data in recommendations:
            recommendation = Recommendation(
                user_id=user.id,
                activity_id=rec_data['activity'].id,
                score=rec_data['score'],
                reasons=rec_data['reasons'],
                ai_explanation=rec_data['ai_explanation']
            )
            self.db.add(recommendation)
        
        self.db.commit()