"""Initial migration

Revision ID: 001_initial
Revises: 
Create Date: 2024-08-19 14:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '001_initial'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Create users table
    op.create_table('users',
    sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('email', sa.String(), nullable=False),
    sa.Column('full_name', sa.String(), nullable=True),
    sa.Column('hashed_password', sa.String(), nullable=False),
    sa.Column('role', sa.Enum('student', 'instructor', 'admin', name='userrole'), nullable=False),
    sa.Column('is_active', sa.Boolean(), nullable=True),
    sa.Column('phone', sa.String(), nullable=True),
    sa.Column('bio', sa.Text(), nullable=True),
    sa.Column('location', sa.String(), nullable=True),
    sa.Column('skills', sa.Text(), nullable=True),
    sa.Column('preferences', sa.Text(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=True)

    # Create locations table
    op.create_table('locations',
    sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('address', sa.String(), nullable=False),
    sa.Column('city', sa.String(), nullable=False),
    sa.Column('postal_code', sa.String(), nullable=False),
    sa.Column('country', sa.String(), nullable=False),
    sa.Column('latitude', sa.Numeric(precision=10, scale=7), nullable=True),
    sa.Column('longitude', sa.Numeric(precision=10, scale=7), nullable=True),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('contact_email', sa.String(), nullable=True),
    sa.Column('contact_phone', sa.String(), nullable=True),
    sa.Column('website', sa.String(), nullable=True),
    sa.Column('image_url', sa.String(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )

    # Create activities table
    op.create_table('activities',
    sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('title', sa.String(), nullable=False),
    sa.Column('slug', sa.String(), nullable=False),
    sa.Column('description', sa.Text(), nullable=False),
    sa.Column('summary', sa.Text(), nullable=True),
    sa.Column('category', sa.String(), nullable=False),
    sa.Column('duration_min', sa.Integer(), nullable=False),
    sa.Column('max_participants', sa.Integer(), nullable=False),
    sa.Column('difficulty_level', sa.Integer(), nullable=False),
    sa.Column('materials', sa.ARRAY(sa.String()), nullable=False),
    sa.Column('skill_tags', sa.ARRAY(sa.String()), nullable=False),
    sa.Column('seasonality', sa.ARRAY(sa.String()), nullable=False),
    sa.Column('safety_level', sa.Integer(), nullable=False),
    sa.Column('location_id', postgresql.UUID(as_uuid=True), nullable=True),
    sa.Column('image_url', sa.String(), nullable=True),
    sa.Column('is_active', sa.Boolean(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['location_id'], ['locations.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_activities_slug'), 'activities', ['slug'], unique=True)

    # Create bookings table
    op.create_table('bookings',
    sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('activity_id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('status', sa.String(), nullable=False),
    sa.Column('start_date', sa.DateTime(), nullable=False),
    sa.Column('end_date', sa.DateTime(), nullable=False),
    sa.Column('participants_count', sa.Integer(), nullable=False),
    sa.Column('notes', sa.Text(), nullable=True),
    sa.Column('cancellation_reason', sa.Text(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['activity_id'], ['activities.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )

    # Create progress table
    op.create_table('progress',
    sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('activity_id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('completed_at', sa.DateTime(), nullable=False),
    sa.Column('rating', sa.Integer(), nullable=True),
    sa.Column('feedback', sa.Text(), nullable=True),
    sa.Column('skills_gained', sa.ARRAY(sa.String()), nullable=False),
    sa.Column('instructor_notes', sa.Text(), nullable=True),
    sa.Column('time_spent_minutes', sa.Integer(), nullable=True),
    sa.Column('achievements', sa.ARRAY(sa.String()), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['activity_id'], ['activities.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )

    # Create messages table
    op.create_table('messages',
    sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('sender_id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('recipient_id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('subject', sa.String(), nullable=False),
    sa.Column('content', sa.Text(), nullable=False),
    sa.Column('read_at', sa.DateTime(), nullable=True),
    sa.Column('reply_to_id', postgresql.UUID(as_uuid=True), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['recipient_id'], ['users.id'], ),
    sa.ForeignKeyConstraint(['reply_to_id'], ['messages.id'], ),
    sa.ForeignKeyConstraint(['sender_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )


def downgrade() -> None:
    op.drop_table('messages')
    op.drop_table('progress')
    op.drop_table('bookings')
    op.drop_index(op.f('ix_activities_slug'), table_name='activities')
    op.drop_table('activities')
    op.drop_table('locations')
    op.drop_index(op.f('ix_users_email'), table_name='users')
    op.drop_table('users')
    op.execute('DROP TYPE userrole')