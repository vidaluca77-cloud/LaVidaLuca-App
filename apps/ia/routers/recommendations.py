from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from models import User, Recommendation
from schemas import Recommendation as RecommendationSchema, RecommendationResponse
from auth import get_current_active_user
from recommendations import RecommendationEngine

router = APIRouter()

@router.get("/", response_model=RecommendationResponse)
async def get_recommendations(
    limit: int = 10,
    regenerate: bool = False,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Obtenir les recommandations pour l'utilisateur actuel"""
    
    if regenerate:
        # Générer de nouvelles recommandations
        engine = RecommendationEngine(db)
        recommendations_data = await engine.get_recommendations(current_user, limit)
        await engine.save_recommendations(current_user, recommendations_data)
        
        # Recharger depuis la base
        recommendations = db.query(Recommendation).filter(
            Recommendation.user_id == current_user.id
        ).order_by(Recommendation.score.desc()).limit(limit).all()
    else:
        # Charger les recommandations existantes
        recommendations = db.query(Recommendation).filter(
            Recommendation.user_id == current_user.id
        ).order_by(Recommendation.score.desc()).limit(limit).all()
        
        # Si aucune recommandation existante, en générer
        if not recommendations:
            engine = RecommendationEngine(db)
            recommendations_data = await engine.get_recommendations(current_user, limit)
            await engine.save_recommendations(current_user, recommendations_data)
            
            recommendations = db.query(Recommendation).filter(
                Recommendation.user_id == current_user.id
            ).order_by(Recommendation.score.desc()).limit(limit).all()
    
    return RecommendationResponse(
        recommendations=recommendations,
        total_count=len(recommendations)
    )

@router.post("/regenerate", response_model=RecommendationResponse)
async def regenerate_recommendations(
    limit: int = 10,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Régénérer les recommandations pour l'utilisateur actuel"""
    engine = RecommendationEngine(db)
    recommendations_data = await engine.get_recommendations(current_user, limit)
    await engine.save_recommendations(current_user, recommendations_data)
    
    recommendations = db.query(Recommendation).filter(
        Recommendation.user_id == current_user.id
    ).order_by(Recommendation.score.desc()).limit(limit).all()
    
    return RecommendationResponse(
        recommendations=recommendations,
        total_count=len(recommendations)
    )