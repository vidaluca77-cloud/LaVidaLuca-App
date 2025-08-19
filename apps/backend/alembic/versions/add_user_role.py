"""Add user role field for enhanced authentication

Revision ID: add_user_role
Revises: 
Create Date: 2024-01-20 12:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'add_user_role'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    """Add role field to users table."""
    # Add role enum type
    user_role_enum = sa.Enum('USER', 'MODERATOR', 'ADMIN', 'SUPERUSER', name='userrole')
    user_role_enum.create(op.get_bind())
    
    # Add role column with default value
    op.add_column('users', sa.Column('role', user_role_enum, nullable=False, server_default='USER'))


def downgrade():
    """Remove role field from users table."""
    op.drop_column('users', 'role')
    
    # Drop enum type
    user_role_enum = sa.Enum('USER', 'MODERATOR', 'ADMIN', 'SUPERUSER', name='userrole')
    user_role_enum.drop(op.get_bind())