"""
Seed script to populate the database with sample data for development and testing.
"""

import asyncio
import sys
import os

# Add the backend directory to the path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy.ext.asyncio import AsyncSession
from database import engine, AsyncSessionLocal
from models.user import User
from models.activity import Activity
from models.contact import Contact
from auth.password import hash_password


async def create_sample_users(session: AsyncSession):
    """Create sample users."""
    users = [
        User(
            email="admin@lavidaluca.fr",
            hashed_password=hash_password("AdminPassword123"),
            first_name="Admin",
            last_name="La Vida Luca",
            is_active=True,
            is_verified=True,
            is_superuser=True,
            profile={
                "skills": ["management", "agriculture", "education"],
                "bio": "Administrateur de la plateforme La Vida Luca",
                "experience_level": "advanced",
            },
        ),
        User(
            email="formateur@lavidaluca.fr",
            hashed_password=hash_password("FormateurPassword123"),
            first_name="Jean",
            last_name="Dubois",
            is_active=True,
            is_verified=True,
            profile={
                "skills": ["apiculture", "jardinage", "permaculture"],
                "interests": ["agriculture biologique", "formation"],
                "location": "Provence, France",
                "bio": "Formateur en agriculture durable et apiculture",
                "experience_level": "expert",
                "preferred_categories": ["agri", "nature"],
            },
        ),
        User(
            email="etudiant@mfr.edu",
            hashed_password=hash_password("EtudiantPassword123"),
            first_name="Marie",
            last_name="Martin",
            is_active=True,
            is_verified=True,
            profile={
                "skills": ["jardinage", "cuisine"],
                "interests": ["agriculture", "artisanat", "cuisine"],
                "location": "Bretagne, France",
                "bio": "Étudiante en formation agricole",
                "experience_level": "beginner",
                "preferred_categories": ["agri", "transfo"],
            },
        ),
    ]

    for user in users:
        session.add(user)

    await session.commit()
    return users


async def create_sample_activities(session: AsyncSession, users):
    """Create sample activities."""
    activities = [
        Activity(
            title="Initiation à l'apiculture",
            category="agri",
            summary="Découverte du monde des abeilles et premiers gestes de l'apiculteur",
            description="""
Cette activité permet aux participants de découvrir l'univers fascinant des abeilles et d'apprendre les bases de l'apiculture. Au programme : observation d'une ruche, identification des différentes castes d'abeilles, manipulation du matériel apicole et récolte de miel.

Les participants apprendront également l'importance des abeilles dans l'écosystème et les enjeux de leur protection.
            """,
            duration_min=180,
            skill_tags=["apiculture", "nature", "biologie", "observation"],
            safety_level=3,
            materials=["combinaison", "enfumoir", "gants", "lève-cadres"],
            difficulty_level=2,
            min_participants=4,
            max_participants=12,
            age_min=14,
            location_type="outdoor",
            location_details="Rucher pédagogique avec ruches d'observation",
            preparation_time=30,
            learning_objectives=[
                "Comprendre l'organisation d'une colonie d'abeilles",
                "Maîtriser les gestes de base de l'apiculteur",
                "Identifier les risques et mesures de sécurité",
            ],
            assessment_methods=["observation pratique", "quiz final"],
            pedagogical_notes="Prévoir une séance théorique en salle avant la pratique",
            is_published=True,
            is_featured=True,
            keywords=["abeilles", "miel", "pollinisation", "biodiversité"],
            season_tags=["spring", "summer"],
            external_resources={
                "videos": ["https://example.com/apiculture-intro"],
                "documents": ["Guide de l'apiculteur débutant"],
            },
            created_by=users[1].id,
        ),
        Activity(
            title="Jardinage en permaculture",
            category="agri",
            summary="Techniques de jardinage respectueuses de l'environnement selon les principes de la permaculture",
            description="""
Atelier pratique sur les techniques de jardinage en permaculture. Les participants apprendront à créer un jardin productif et durable en travaillant avec la nature plutôt que contre elle.

Au programme : design du jardin, associations de plantes, compostage, gestion de l'eau, et création de buttes de culture.
            """,
            duration_min=240,
            skill_tags=["jardinage", "permaculture", "écologie", "design"],
            safety_level=1,
            materials=["bêche", "serfouette", "arrosoir", "graines", "compost"],
            difficulty_level=1,
            min_participants=6,
            max_participants=15,
            age_min=12,
            location_type="outdoor",
            location_details="Jardin pédagogique avec différentes zones de culture",
            preparation_time=45,
            learning_objectives=[
                "Comprendre les principes de la permaculture",
                "Savoir créer des associations de plantes",
                "Maîtriser les techniques de compostage",
            ],
            assessment_methods=["réalisation pratique", "présentation orale"],
            is_published=True,
            is_featured=True,
            keywords=["permaculture", "biodiversité", "durabilité"],
            season_tags=["spring", "summer", "autumn"],
            created_by=users[1].id,
        ),
        Activity(
            title="Fabrication de fromage artisanal",
            category="transfo",
            summary="Apprentissage des techniques traditionnelles de fabrication fromagère",
            description="""
Atelier de transformation laitière où les participants découvrent les secrets de la fabrication du fromage. De la traite à l'affinage, toutes les étapes seront abordées dans le respect des traditions fromagères.

Les participants repartiront avec leurs propres fromages et les connaissances pour reproduire l'expérience chez eux.
            """,
            duration_min=300,
            skill_tags=["fromagerie", "transformation", "tradition", "hygiène"],
            safety_level=2,
            materials=["lait", "présure", "ferments", "moules", "égouttoirs"],
            difficulty_level=3,
            min_participants=4,
            max_participants=10,
            age_min=16,
            location_type="indoor",
            location_details="Atelier de transformation avec équipement professionnel",
            preparation_time=60,
            learning_objectives=[
                "Maîtriser les étapes de fabrication du fromage",
                "Comprendre l'importance de l'hygiène",
                "Connaître les techniques d'affinage",
            ],
            assessment_methods=["réalisation pratique", "dégustation"],
            is_published=True,
            keywords=["fromage", "lait", "tradition", "savoir-faire"],
            season_tags=["autumn", "winter"],
            created_by=users[0].id,
        ),
        Activity(
            title="Poterie traditionnelle",
            category="artisanat",
            summary="Initiation aux techniques de poterie selon les méthodes ancestrales",
            description="""
Découverte de l'art de la poterie à travers les techniques traditionnelles. Les participants apprendront à travailler l'argile, à façonner des objets utilitaires et décoratifs, et à comprendre les secrets de la cuisson.

Cet atelier permet de renouer avec un savoir-faire ancestral tout en développant sa créativité.
            """,
            duration_min=240,
            skill_tags=["poterie", "artisanat", "créativité", "tradition"],
            safety_level=2,
            materials=["argile", "outils de modelage", "tour de potier", "émail"],
            difficulty_level=2,
            min_participants=3,
            max_participants=8,
            age_min=10,
            location_type="workshop",
            location_details="Atelier de poterie avec tours et four",
            preparation_time=30,
            learning_objectives=[
                "Maîtriser les techniques de base du tournage",
                "Comprendre le processus de cuisson",
                "Développer sa créativité artistique",
            ],
            assessment_methods=["réalisation d'une pièce", "auto-évaluation"],
            is_published=True,
            keywords=["argile", "créativité", "artisanat", "tradition"],
            season_tags=["autumn", "winter"],
            created_by=users[1].id,
        ),
        Activity(
            title="Observation de la faune locale",
            category="nature",
            summary="Sortie naturaliste pour découvrir et identifier la faune de la région",
            description="""
Sortie d'observation et d'identification de la faune locale. Les participants apprendront à reconnaître les espèces animales de leur région, à comprendre leurs habitats et leurs comportements.

Une belle occasion de développer son sens de l'observation et sa connaissance de la biodiversité locale.
            """,
            duration_min=180,
            skill_tags=["observation", "faune", "biodiversité", "identification"],
            safety_level=1,
            materials=["jumelles", "guide d'identification", "carnet d'observation"],
            difficulty_level=1,
            min_participants=5,
            max_participants=20,
            age_min=8,
            location_type="outdoor",
            location_details="Parc naturel ou zone forestière",
            preparation_time=15,
            learning_objectives=[
                "Savoir identifier les principales espèces locales",
                "Comprendre les écosystèmes naturels",
                "Développer l'observation naturaliste",
            ],
            assessment_methods=["carnet d'observation", "présentation d'espèce"],
            is_published=True,
            keywords=["faune", "nature", "observation", "biodiversité"],
            season_tags=["spring", "summer", "autumn"],
            created_by=users[1].id,
        ),
    ]

    for activity in activities:
        session.add(activity)

    await session.commit()
    return activities


async def create_sample_contacts(session: AsyncSession):
    """Create sample contact requests."""
    contacts = [
        Contact(
            name="Pierre Dupont",
            email="pierre.dupont@mfr-example.fr",
            phone="+33123456789",
            organization="MFR de Provence",
            subject="Demande de partenariat",
            message="Bonjour, notre MFR souhaiterait établir un partenariat avec La Vida Luca pour enrichir notre offre pédagogique. Pouvons-nous organiser une rencontre pour discuter des modalités ?",
            contact_type="partnership",
            status="new",
            priority="normal",
            consent_privacy=True,
            metadata={"source": "website", "referrer": "google"},
        ),
        Contact(
            name="Sophie Martin",
            email="sophie.martin@gmail.com",
            subject="Question sur les formations",
            message="Je suis intéressée par vos formations en agriculture durable. Proposez-vous des modules pour adultes en reconversion professionnelle ?",
            contact_type="general",
            status="in_progress",
            priority="normal",
            consent_privacy=True,
            consent_marketing=True,
        ),
        Contact(
            name="Lucas Bernard",
            email="lucas.bernard@email.fr",
            phone="+33987654321",
            subject="Proposition d'intervention",
            message="Bonjour, je suis apiculteur professionnel et je propose mes services pour animer des ateliers d'initiation à l'apiculture dans vos formations.",
            contact_type="collaboration",
            status="resolved",
            priority="high",
            is_responded=True,
            response_count=2,
            consent_privacy=True,
            tags=["apiculture", "formateur"],
        ),
    ]

    for contact in contacts:
        session.add(contact)

    await session.commit()
    return contacts


async def seed_database():
    """Main function to seed the database with sample data."""
    print("🌱 Seeding database with sample data...")

    async with AsyncSessionLocal() as session:
        try:
            # Create sample data
            print("👤 Creating sample users...")
            users = await create_sample_users(session)
            print(f"✅ Created {len(users)} users")

            print("📚 Creating sample activities...")
            activities = await create_sample_activities(session, users)
            print(f"✅ Created {len(activities)} activities")

            print("📞 Creating sample contacts...")
            contacts = await create_sample_contacts(session)
            print(f"✅ Created {len(contacts)} contacts")

            print("\n🎉 Database seeded successfully!")
            print("\nSample credentials:")
            print("Admin: admin@lavidaluca.fr / AdminPassword123")
            print("Trainer: formateur@lavidaluca.fr / FormateurPassword123")
            print("Student: etudiant@mfr.edu / EtudiantPassword123")

        except Exception as e:
            print(f"❌ Error seeding database: {e}")
            await session.rollback()
            raise


if __name__ == "__main__":
    asyncio.run(seed_database())
