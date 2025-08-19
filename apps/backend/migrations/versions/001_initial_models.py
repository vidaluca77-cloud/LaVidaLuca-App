"""Initial migration with comprehensive models

Revision ID: 001_initial_models
Revises: 
Create Date: 2025-01-28 10:00:00.000000

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '001_initial_models'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Create all tables with proper structure."""
    # ### Users table ###
    op.create_table('users',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('email', sa.String(length=255), nullable=False),
        sa.Column('hashed_password', sa.String(length=255), nullable=False),
        sa.Column('role', sa.String(length=50), nullable=False, server_default='user'),
        sa.Column('first_name', sa.String(length=100), nullable=True),
        sa.Column('last_name', sa.String(length=100), nullable=True),
        sa.Column('profile', sa.JSON(), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=True, server_default='true'),
        sa.Column('is_verified', sa.Boolean(), nullable=True, server_default='false'),
        sa.Column('is_superuser', sa.Boolean(), nullable=True, server_default='false'),
        sa.Column('last_login', sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_users_email', 'users', ['email'], unique=True)
    op.create_index('ix_users_email_active', 'users', ['email', 'is_active'], unique=False)
    op.create_index('ix_users_role', 'users', ['role'], unique=False)
    op.create_index('ix_users_last_login', 'users', ['last_login'], unique=False)

    # ### Activities table ###
    op.create_table('activities',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('title', sa.String(length=255), nullable=False),
        sa.Column('category', sa.String(length=50), nullable=False),
        sa.Column('summary', sa.Text(), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('duration_min', sa.Integer(), nullable=False),
        sa.Column('skill_tags', postgresql.ARRAY(sa.String()), nullable=True),
        sa.Column('safety_level', sa.Integer(), nullable=True, server_default='1'),
        sa.Column('materials', postgresql.ARRAY(sa.String()), nullable=True),
        sa.Column('difficulty_level', sa.Integer(), nullable=True, server_default='1'),
        sa.Column('min_participants', sa.Integer(), nullable=True, server_default='1'),
        sa.Column('max_participants', sa.Integer(), nullable=True),
        sa.Column('age_min', sa.Integer(), nullable=True),
        sa.Column('age_max', sa.Integer(), nullable=True),
        sa.Column('location_type', sa.String(length=50), nullable=True),
        sa.Column('location_details', sa.Text(), nullable=True),
        sa.Column('preparation_time', sa.Integer(), nullable=True, server_default='0'),
        sa.Column('learning_objectives', postgresql.ARRAY(sa.String()), nullable=True),
        sa.Column('assessment_methods', postgresql.ARRAY(sa.String()), nullable=True),
        sa.Column('pedagogical_notes', sa.Text(), nullable=True),
        sa.Column('created_by', postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column('is_published', sa.Boolean(), nullable=True, server_default='true'),
        sa.Column('is_featured', sa.Boolean(), nullable=True, server_default='false'),
        sa.Column('keywords', postgresql.ARRAY(sa.String()), nullable=True),
        sa.Column('season_tags', postgresql.ARRAY(sa.String()), nullable=True),
        sa.Column('external_resources', sa.JSON(), nullable=True),
        sa.Column('metadata', sa.JSON(), nullable=True),
        sa.ForeignKeyConstraint(['created_by'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_activities_category', 'activities', ['category'], unique=False)
    op.create_index('ix_activities_difficulty_level', 'activities', ['difficulty_level'], unique=False)
    op.create_index('ix_activities_is_published', 'activities', ['is_published'], unique=False)
    op.create_index('ix_activities_is_featured', 'activities', ['is_featured'], unique=False)
    op.create_index('ix_activities_title_search', 'activities', ['title'], unique=False)
    op.create_index('ix_activities_category_published', 'activities', ['category', 'is_published'], unique=False)
    op.create_index('ix_activities_difficulty_published', 'activities', ['difficulty_level', 'is_published'], unique=False)
    op.create_index('ix_activities_duration', 'activities', ['duration_min'], unique=False)
    op.create_index('ix_activities_age_range', 'activities', ['age_min', 'age_max'], unique=False)
    op.create_index('ix_activities_creator', 'activities', ['created_by'], unique=False)

    # ### Contacts table ###
    op.create_table('contacts',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('email', sa.String(length=255), nullable=False),
        sa.Column('phone', sa.String(length=50), nullable=True),
        sa.Column('organization', sa.String(length=255), nullable=True),
        sa.Column('subject', sa.String(length=500), nullable=False),
        sa.Column('message', sa.Text(), nullable=False),
        sa.Column('contact_type', sa.String(length=50), nullable=True, server_default='general'),
        sa.Column('status', sa.String(length=50), nullable=True, server_default='new'),
        sa.Column('priority', sa.String(length=20), nullable=True, server_default='normal'),
        sa.Column('assigned_to', postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column('is_responded', sa.Boolean(), nullable=True, server_default='false'),
        sa.Column('response_count', sa.Integer(), nullable=True, server_default='0'),
        sa.Column('last_response_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('metadata', sa.JSON(), nullable=True),
        sa.Column('tags', postgresql.ARRAY(sa.String()), nullable=True),
        sa.Column('consent_privacy', sa.Boolean(), nullable=True, server_default='true'),
        sa.Column('consent_marketing', sa.Boolean(), nullable=True, server_default='false'),
        sa.ForeignKeyConstraint(['assigned_to'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_contacts_email', 'contacts', ['email'], unique=False)
    op.create_index('ix_contacts_contact_type', 'contacts', ['contact_type'], unique=False)
    op.create_index('ix_contacts_status', 'contacts', ['status'], unique=False)
    op.create_index('ix_contacts_is_responded', 'contacts', ['is_responded'], unique=False)
    op.create_index('ix_contacts_email_type', 'contacts', ['email', 'contact_type'], unique=False)
    op.create_index('ix_contacts_status_priority', 'contacts', ['status', 'priority'], unique=False)
    op.create_index('ix_contacts_assigned_status', 'contacts', ['assigned_to', 'status'], unique=False)
    op.create_index('ix_contacts_created_status', 'contacts', ['created_at', 'status'], unique=False)
    op.create_index('ix_contacts_response_tracking', 'contacts', ['is_responded', 'last_response_at'], unique=False)


def downgrade() -> None:
    """Drop all tables."""
    op.drop_table('contacts')
    op.drop_table('activities')
    op.drop_table('users')