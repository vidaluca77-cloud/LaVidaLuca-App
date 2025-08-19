"""Add profile model

Revision ID: add_profile_model
Revises: 50b8a4156bf7
Create Date: 2025-08-19 22:30:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID, ARRAY


# revision identifiers, used by Alembic.
revision: str = 'add_profile_model'
down_revision: Union[str, None] = '50b8a4156bf7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Update users table to use UUID and add profile relationship support
    op.execute('CREATE EXTENSION IF NOT EXISTS "uuid-ossp"')
    
    # Create profiles table
    op.create_table('profiles',
        sa.Column('id', UUID(as_uuid=True), primary_key=True, server_default=sa.text('uuid_generate_v4()')),
        sa.Column('user_id', UUID(as_uuid=True), sa.ForeignKey('users.id'), unique=True, nullable=False),
        
        # Core profile information
        sa.Column('skills', ARRAY(sa.String), default=[], nullable=True),
        sa.Column('availability', ARRAY(sa.String), default=[], nullable=True),
        sa.Column('location', sa.String(255), nullable=True),
        sa.Column('preferences', ARRAY(sa.String), default=[], nullable=True),
        
        # Experience and education
        sa.Column('experience_level', sa.String(50), default='beginner', nullable=True),
        sa.Column('education_background', ARRAY(sa.String), default=[], nullable=True),
        sa.Column('certifications', ARRAY(sa.String), default=[], nullable=True),
        
        # Learning preferences
        sa.Column('learning_style', ARRAY(sa.String), default=[], nullable=True),
        sa.Column('preferred_activity_types', ARRAY(sa.String), default=[], nullable=True),
        sa.Column('preferred_group_size', sa.String(20), nullable=True),
        
        # Availability details
        sa.Column('time_availability', sa.JSON, default={}, nullable=True),
        sa.Column('seasonal_availability', ARRAY(sa.String), default=[], nullable=True),
        
        # Interests and goals
        sa.Column('interests', ARRAY(sa.String), default=[], nullable=True),
        sa.Column('learning_goals', ARRAY(sa.String), default=[], nullable=True),
        sa.Column('career_goals', ARRAY(sa.String), default=[], nullable=True),
        
        # Safety and accessibility
        sa.Column('physical_limitations', ARRAY(sa.String), default=[], nullable=True),
        sa.Column('safety_preferences', sa.JSON, default={}, nullable=True),
        sa.Column('accessibility_needs', ARRAY(sa.String), default=[], nullable=True),
        
        # Social preferences
        sa.Column('mentoring_interest', sa.Boolean, default=False, nullable=True),
        sa.Column('collaboration_preference', sa.String(20), default='flexible', nullable=True),
        sa.Column('communication_style', ARRAY(sa.String), default=[], nullable=True),
        
        # Geographic and logistics
        sa.Column('travel_willingness', sa.String(20), default='local', nullable=True),
        sa.Column('transportation_access', ARRAY(sa.String), default=[], nullable=True),
        
        # Additional flexible data
        sa.Column('custom_fields', sa.JSON, default={}, nullable=True),
        
        # Profile completion and settings
        sa.Column('is_complete', sa.Boolean, default=False, nullable=True),
        sa.Column('is_public', sa.Boolean, default=True, nullable=True),
        
        # Timestamps
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), onupdate=sa.func.now(), nullable=True),
    )
    
    # Create indexes for better query performance
    op.create_index('ix_profiles_user_id', 'profiles', ['user_id'])
    op.create_index('ix_profiles_location', 'profiles', ['location'])
    op.create_index('ix_profiles_experience_level', 'profiles', ['experience_level'])
    op.create_index('ix_profiles_is_public', 'profiles', ['is_public'])


def downgrade() -> None:
    # Drop indexes
    op.drop_index('ix_profiles_is_public', 'profiles')
    op.drop_index('ix_profiles_experience_level', 'profiles')
    op.drop_index('ix_profiles_location', 'profiles')
    op.drop_index('ix_profiles_user_id', 'profiles')
    
    # Drop table
    op.drop_table('profiles')