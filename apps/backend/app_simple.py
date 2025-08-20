"""
Simple working FastAPI app for La Vida Luca.
This version bypasses the complex import structure for now.
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import logging
import os

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="La Vida Luca API",
    description="API pour la plateforme collaborative La Vida Luca",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class GuideRequest(BaseModel):
    """Request model for guide endpoint."""
    question: str
    context: Optional[str] = None


class GuideResponse(BaseModel):
    """Response model for guide endpoint."""
    answer: str
    confidence: Optional[float] = None
    sources: Optional[list[str]] = None


class AgricultureRequest(BaseModel):
    """Request model for agricultural assistant."""
    question: str
    context: Optional[str] = None
    location: Optional[str] = None
    crop_type: Optional[str] = None


class AgricultureResponse(BaseModel):
    """Response model for agricultural assistant."""
    answer: str
    category: Optional[str] = None
    tags: list[str] = []
    response_time: str
    confidence: Optional[float] = None


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "Welcome to La Vida Luca API",
        "version": "1.0.0",
        "docs": "/docs",
        "status": "healthy"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "database": "not_connected",  # Simplified for now
        "environment": os.getenv("ENVIRONMENT", "development")
    }


@app.post("/api/v1/guide", response_model=GuideResponse)
async def get_guide(request: GuideRequest):
    """
    Get AI-powered guidance for questions about sustainable living and gardening.
    """
    try:
        # Generate response based on question content
        if "sol" in request.question.lower() or "terre" in request.question.lower():
            answer = """Pour améliorer un sol argileux compact, voici quelques conseils :

1. **Ajouter de la matière organique** : Incorporez du compost, du fumier bien décomposé ou des feuilles mortes pour améliorer la structure du sol.

2. **Éviter le travail du sol humide** : Ne jamais travailler un sol argileux quand il est détrempé, cela créerait des mottes très dures.

3. **Créer des buttes de culture** : Surélevez vos zones de plantation pour améliorer le drainage.

4. **Planter des couvre-sols** : Utilisez des plantes comme la luzerne ou le trèfle pour structurer naturellement le sol.

5. **Paillis permanent** : Gardez le sol couvert pour protéger sa structure et nourrir la vie microbienne.

Ces méthodes améliorent progressivement la texture et la fertilité de votre sol argileux."""
            
        elif "jardinage" in request.question.lower() or "plante" in request.question.lower():
            answer = """Pour réussir votre jardinage, voici des conseils de base :

1. **Connaître son sol** : Testez le pH et la composition de votre terre
2. **Choisir les bonnes plantes** : Adaptées à votre climat et exposition
3. **Planifier les rotations** : Alternez les familles de légumes
4. **Arroser intelligemment** : Le matin de préférence, au pied des plantes
5. **Composter** : Recyclez vos déchets verts pour nourrir le sol

Besoin de conseils plus spécifiques ? N'hésitez pas à préciser votre question !"""
        
        elif "compost" in request.question.lower():
            answer = """Voici comment faire un compost efficace :

1. **Équilibrer vert et brun** : 1/3 de matières azotées (épluchures, tontes) pour 2/3 de matières carbonées (feuilles sèches, carton)

2. **Surveiller l'humidité** : Le compost doit être humide comme une éponge essorée

3. **Aérer régulièrement** : Retournez le tas toutes les 2-3 semaines

4. **Température idéale** : 50-60°C au centre indique une bonne décomposition

5. **Patience** : Comptez 6-12 mois selon les conditions

Un bon compost sent la terre de forêt, pas l'ammoniaque !"""
        
        else:
            answer = f"""Merci pour votre question : "{request.question}"

Je suis là pour vous aider avec des conseils sur :
- Le jardinage et la permaculture
- La vie durable et écologique  
- Les initiatives communautaires locales
- La préservation de l'environnement

Pouvez-vous préciser votre domaine d'intérêt pour que je puisse vous donner des conseils plus adaptés ?"""

        return GuideResponse(
            answer=answer,
            confidence=0.8,
            sources=["La Vida Luca Knowledge Base", "Sustainable Living Practices"]
        )
        
    except Exception as e:
        logger.error(f"Error in guide endpoint: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="Une erreur est survenue lors du traitement de votre question"
        )


@app.get("/api/v1/guide/health")
async def guide_health():
    """Health check for guide service."""
    return {
        "status": "healthy",
        "service": "guide",
        "ai_enabled": os.getenv("OPENAI_API_KEY") is not None
    }


@app.post("/api/v1/consultations/ask", response_model=AgricultureResponse)
async def agricultural_assistant(request: AgricultureRequest):
    """
    Agricultural AI assistant for answering farming questions.
    """
    import time
    start_time = time.time()
    
    try:
        # Analyze the question to determine category and generate appropriate response
        question_lower = request.question.lower()
        
        # Determine category based on keywords
        if any(word in question_lower for word in ['permaculture', 'biologique', 'durable', 'écologique']):
            category = 'permaculture'
        elif any(word in question_lower for word in ['culture', 'plante', 'semis', 'récolte', 'rotation']):
            category = 'crop_management'
        elif any(word in question_lower for word in ['animal', 'élevage', 'bétail', 'volaille']):
            category = 'animal_health'
        elif any(word in question_lower for word in ['sol', 'compost', 'fertilisant', 'terre']):
            category = 'soil_management'
        elif any(word in question_lower for word in ['parasite', 'maladie', 'insecte', 'traitement']):
            category = 'pest_control'
        elif any(word in question_lower for word in ['eau', 'irrigation', 'arrosage']):
            category = 'irrigation'
        else:
            category = 'general'
        
        # Generate response based on category and keywords
        if category == 'soil_management' or 'sol' in question_lower:
            answer = """🌱 **Amélioration des sols agricoles**

Pour optimiser la qualité de votre sol :

**1. Analyse du sol**
- Testez le pH (idéal : 6,0-7,0 pour la plupart des cultures)
- Vérifiez la teneur en matière organique (objectif : 3-5%)
- Évaluez la structure et le drainage

**2. Enrichissement naturel**
- Compost mûr : 20-30 tonnes/hectare/an
- Fumier bien décomposé : améliore la structure
- Couverture végétale permanente : protège et nourrit

**3. Techniques biologiques**
- Rotation des cultures : évite l'épuisement
- Cultures d'engrais verts : luzerne, trèfle, moutarde
- Réduction du travail du sol : préserve la vie microbienne

**4. Gestion de l'eau**
- Drainage adapté selon le type de sol
- Irrigation raisonnée pour éviter le lessivage
- Paillage pour retenir l'humidité

Un sol vivant et fertile est la base d'une agriculture durable !"""
            tags = ['sol', 'fertilité', 'compost', 'analyse']
            
        elif category == 'crop_management' or any(word in question_lower for word in ['tomate', 'légume', 'culture']):
            answer = """🍅 **Gestion des cultures**

Conseils pour une production optimale :

**1. Planification**
- Rotation 4 ans minimum : légumes-feuilles → légumineuses → légumes-racines → céréales
- Associations bénéfiques : tomates + basilic, courges + haricots + maïs
- Calendrier de semis adapté à votre région

**2. Techniques culturales**
- Semis en pépinière pour les plants exigeants
- Transplantation quand les risques de gel sont écartés
- Espacement respecté pour éviter la concurrence

**3. Suivi sanitaire**
- Observation quotidienne des cultures
- Traitement préventif naturel (purins d'ortie, prêle)
- Élimination rapide des plants malades

**4. Récolte optimisée**
- Récolte au bon stade de maturité
- Horaires frais (matin/soir) pour préserver la qualité
- Conservation adaptée selon le légume

Une approche préventive vaut mieux qu'un traitement curatif !"""
            tags = ['cultures', 'rotation', 'association', 'récolte']
            
        elif category == 'pest_control' or any(word in question_lower for word in ['parasite', 'maladie', 'puceron']):
            answer = """🐛 **Lutte biologique contre les ravageurs**

Solutions naturelles et durables :

**1. Prévention**
- Biodiversité : haies, fleurs mellifères, nichoirs
- Plantes répulsives : tanaisie, lavande, œillets d'Inde
- Hygiène culturale : élimination des déchets infectés

**2. Auxiliaires naturels**
- Coccinelles contre les pucerons
- Chrysopes contre les thrips
- Oiseaux insectivores : mésanges, rouge-gorge

**3. Traitements biologiques**
- Purin d'ortie : répulsif et fertilisant (dilution 10%)
- Décoction de prêle : fongicide naturel
- Savon noir : contre pucerons et acariens

**4. Barrières physiques**
- Voiles anti-insectes pour protections directes
- Pièges chromatiques : jaunes pour pucerons, bleus pour thrips
- Mulch répulsif : copeaux de cèdre

L'équilibre naturel est votre meilleur allié !"""
            tags = ['biocontrôle', 'auxiliaires', 'prévention', 'purin']
            
        elif category == 'permaculture':
            answer = """🌿 **Principes de permaculture**

Créer un système agricole durable :

**1. Observation et design**
- Analysez votre terrain : exposition, dénivelé, microclimat
- Zonage : zones intensives près de la maison, extensives en périphérie
- Flux d'énergie et circuits courts

**2. Diversité et résilience**
- Polyculture vs monoculture
- Étagement vertical : arbres, arbustes, herbacées, couvre-sol
- Écosystèmes autonomes et auto-régulés

**3. Gestion de l'eau**
- Récupération d'eau de pluie
- Swales et bassins de rétention
- Irrigation gravitaire

**4. Cycles fermés**
- Compostage de tous les déchets organiques
- Intégration animaux-végétaux
- Valorisation énergétique (biogaz, solaire)

**5. Sols vivants**
- Jamais de sol nu
- Apports organiques permanents
- Minimal intervention

La permaculture imite les écosystèmes naturels pour une productivité durable !"""
            tags = ['permaculture', 'design', 'durabilité', 'écosystème']
            
        elif category == 'animal_health':
            answer = """🐄 **Santé animale en élevage durable**

Approche préventive et naturelle :

**1. Bien-être animal**
- Espace suffisant : 2-3x les normes conventionnelles
- Accès au plein air et à l'ombre
- Enrichissement du milieu de vie

**2. Alimentation naturelle**
- Pâturages diversifiés : graminées + légumineuses
- Foin de qualité en complément
- Eau propre et accessible en permanence

**3. Prévention sanitaire**
- Quarantaine pour nouveaux animaux
- Observation quotidienne du comportement
- Rotation des pâtures contre le parasitisme

**4. Médecines alternatives**
- Phytothérapie : échinacée, ail, thym
- Aromathérapie pour stress et infections
- Homéopathie en complément

**5. Gestion du troupeau**
- Sélection d'races rustiques adaptées
- Reproduction naturelle privilégiée
- Abattage stress-free

Un animal en bonne santé dans un environnement adapté produit mieux !"""
            tags = ['bien-être', 'prévention', 'phytothérapie', 'pâturage']
            
        else:
            answer = f"""🌾 **Assistant Agricole La Vida Luca**

Merci pour votre question : "{request.question}"

Je suis spécialisé dans l'accompagnement agricole durable. Mes domaines d'expertise :

🌱 **Gestion des sols** : fertilité, compostage, analyses
🍅 **Cultures** : rotation, associations, calendrier cultural
🐛 **Biocontrôle** : lutte naturelle contre ravageurs et maladies
🌿 **Permaculture** : design écologique, autonomie alimentaire
🐄 **Élevage durable** : bien-être animal, médecines naturelles
💧 **Irrigation** : économie d'eau, techniques adaptées
🌡️ **Adaptation climatique** : variétés résistantes, microclimats

**Posez-moi une question plus spécifique** pour obtenir des conseils pratiques adaptés à votre situation !

Exemples :
- "Comment améliorer un sol argileux ?"
- "Quelles associations de légumes dans mon potager ?"
- "Comment lutter contre les pucerons naturellement ?"
- "Quelle rotation pour mes parcelles céréalières ?"
"""
            tags = ['conseil', 'agriculture', 'durable']
        
        response_time = f"{(time.time() - start_time):.2f}s"
        
        return AgricultureResponse(
            answer=answer,
            category=category,
            tags=tags,
            response_time=response_time,
            confidence=0.85
        )
        
    except Exception as e:
        logger.error(f"Error in agricultural assistant: {str(e)}")
        response_time = f"{(time.time() - start_time):.2f}s"
        raise HTTPException(
            status_code=500,
            detail="Une erreur est survenue lors du traitement de votre question agricole"
        )


@app.get("/api/v1/consultations/categories")
async def get_agriculture_categories():
    """Get available agricultural consultation categories."""
    return {
        "categories": [
            {
                "id": "soil_management",
                "name": "Gestion des sols",
                "description": "Fertilité, compostage, analyses de sol",
                "icon": "🌱"
            },
            {
                "id": "crop_management", 
                "name": "Gestion des cultures",
                "description": "Rotation, associations, calendrier cultural",
                "icon": "🍅"
            },
            {
                "id": "pest_control",
                "name": "Biocontrôle",
                "description": "Lutte naturelle contre ravageurs et maladies",
                "icon": "🐛"
            },
            {
                "id": "permaculture",
                "name": "Permaculture",
                "description": "Design écologique, autonomie alimentaire",
                "icon": "🌿"
            },
            {
                "id": "animal_health",
                "name": "Élevage durable",
                "description": "Bien-être animal, médecines naturelles",
                "icon": "🐄"
            },
            {
                "id": "irrigation",
                "name": "Irrigation",
                "description": "Économie d'eau, techniques adaptées",
                "icon": "💧"
            },
            {
                "id": "climate_adaptation",
                "name": "Adaptation climatique",
                "description": "Variétés résistantes, microclimats",
                "icon": "🌡️"
            }
        ]
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)