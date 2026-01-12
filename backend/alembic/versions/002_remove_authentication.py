"""Remove authentication

Revision ID: 002_remove_auth
Revises: 001_initial
Create Date: 2024-01-02 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '002_remove_auth'
down_revision = '001_initial'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Drop foreign key constraint from analyses table
    op.drop_constraint('analyses_user_id_fkey', 'analyses', type_='foreignkey')
    
    # Drop user_id column from analyses table
    op.drop_column('analyses', 'user_id')
    
    # Drop users table
    op.drop_index(op.f('ix_users_email'), table_name='users')
    op.drop_index(op.f('ix_users_id'), table_name='users')
    op.drop_table('users')


def downgrade() -> None:
    # Recreate users table
    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('email', sa.String(), nullable=False),
        sa.Column('password_hash', sa.String(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_users_id'), 'users', ['id'], unique=False)
    op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=True)
    
    # Recreate user_id column in analyses table
    op.add_column('analyses', sa.Column('user_id', sa.Integer(), nullable=False, server_default='1'))
    op.create_foreign_key('analyses_user_id_fkey', 'analyses', 'users', ['user_id'], ['id'])

