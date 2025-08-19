import openai
import os
from typing import List, Dict, Any
from dotenv import load_dotenv

load_dotenv()

class OpenAIService:
    def __init__(self):
        self.client = openai.OpenAI(
            api_key=os.getenv("OPENAI_API_KEY")
        )
    
    async def generate_activity_suggestions(
        self, 
        user_profile: Dict[str, Any], 
        context: str = ""
    ) -> List[str]:
        """
        Generate personalized activity suggestions using OpenAI.
        """
        prompt = self._build_suggestion_prompt(user_profile, context)
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "system",
                        "content": "Tu es un conseiller pédagogique spécialisé dans l'agriculture et la formation en MFR (Maison Familiale Rurale). Tu donnes des conseils personnalisés pour des activités agricoles, artisanales et environnementales."
                    },
                    {
                        "role": "user", 
                        "content": prompt
                    }
                ],
                max_tokens=500,
                temperature=0.7
            )
            
            content = response.choices[0].message.content
            # Parse the response into suggestions
            suggestions = [s.strip() for s in content.split('\n') if s.strip() and not s.strip().startswith('-')]
            return suggestions[:5]  # Return top 5 suggestions
            
        except Exception as e:
            print(f"OpenAI API error: {e}")
            return ["Désolé, nous ne pouvons pas générer de suggestions pour le moment."]
    
    async def analyze_user_learning_path(
        self,
        user_skills: List[str],
        completed_activities: List[str],
        goals: str = ""
    ) -> Dict[str, Any]:
        """
        Analyze user's learning progress and suggest next steps.
        """
        prompt = self._build_analysis_prompt(user_skills, completed_activities, goals)
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "system",
                        "content": "Tu es un analyste pédagogique spécialisé dans l'agriculture. Tu analyses les parcours d'apprentissage et donnes des recommandations pour progresser."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                max_tokens=400,
                temperature=0.6
            )
            
            content = response.choices[0].message.content
            
            return {
                "analysis": content,
                "strengths": self._extract_strengths(content),
                "next_steps": self._extract_next_steps(content),
                "learning_level": self._assess_learning_level(user_skills, completed_activities)
            }
            
        except Exception as e:
            print(f"OpenAI API error: {e}")
            return {
                "analysis": "Analyse temporairement indisponible.",
                "strengths": [],
                "next_steps": [],
                "learning_level": "beginner"
            }
    
    async def generate_activity_description(
        self,
        activity_title: str,
        category: str,
        duration: int,
        safety_level: int
    ) -> str:
        """
        Generate a detailed description for an activity.
        """
        prompt = f"""
        Génère une description détaillée et engageante pour cette activité agricole/artisanale :
        
        Titre : {activity_title}
        Catégorie : {category}
        Durée : {duration} minutes
        Niveau de sécurité : {safety_level}/5
        
        La description doit inclure :
        - Les objectifs pédagogiques
        - Les étapes principales
        - Les compétences développées
        - Les précautions de sécurité
        - L'intérêt pratique
        
        Style : accessible et motivant pour des jeunes en formation.
        """
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "system",
                        "content": "Tu es un rédacteur pédagogique spécialisé dans l'agriculture et la formation professionnelle."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                max_tokens=600,
                temperature=0.7
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            print(f"OpenAI API error: {e}")
            return "Description détaillée à venir."
    
    def _build_suggestion_prompt(self, user_profile: Dict[str, Any], context: str) -> str:
        """Build prompt for activity suggestions."""
        prompt = f"""
        Profil utilisateur :
        - Compétences : {', '.join(user_profile.get('skills', []))}
        - Disponibilités : {', '.join(user_profile.get('availability', []))}
        - Préférences : {', '.join(user_profile.get('preferences', []))}
        - Localisation : {user_profile.get('location', 'Non spécifiée')}
        - Élève MFR : {'Oui' if user_profile.get('is_student', False) else 'Non'}
        
        Contexte : {context}
        
        Suggère 3-5 activités agricoles/artisanales personnalisées qui correspondent à ce profil.
        Chaque suggestion doit être concise (1-2 phrases) et expliquer pourquoi elle convient.
        """
        return prompt
    
    def _build_analysis_prompt(self, skills: List[str], completed: List[str], goals: str) -> str:
        """Build prompt for learning path analysis."""
        prompt = f"""
        Analyse ce parcours d'apprentissage :
        
        Compétences acquises : {', '.join(skills) if skills else 'Aucune'}
        Activités complétées : {', '.join(completed) if completed else 'Aucune'}
        Objectifs : {goals if goals else 'Non spécifiés'}
        
        Analyse :
        1. Points forts du parcours
        2. Domaines à développer
        3. Prochaines étapes recommandées
        4. Progression pédagogique
        
        Réponds de manière structurée et encourageante.
        """
        return prompt
    
    def _extract_strengths(self, content: str) -> List[str]:
        """Extract strengths from analysis content."""
        # Simple extraction - could be enhanced with better parsing
        lines = content.split('\n')
        strengths = []
        for line in lines:
            if 'point fort' in line.lower() or 'compétence' in line.lower():
                strengths.append(line.strip())
        return strengths[:3]
    
    def _extract_next_steps(self, content: str) -> List[str]:
        """Extract next steps from analysis content."""
        lines = content.split('\n')
        steps = []
        for line in lines:
            if 'prochaine' in line.lower() or 'recommand' in line.lower():
                steps.append(line.strip())
        return steps[:3]
    
    def _assess_learning_level(self, skills: List[str], completed: List[str]) -> str:
        """Assess user's learning level based on skills and completed activities."""
        total_progress = len(skills) + len(completed)
        
        if total_progress < 3:
            return "beginner"
        elif total_progress < 10:
            return "intermediate"
        else:
            return "advanced"