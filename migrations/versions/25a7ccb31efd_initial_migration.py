"""Initial migration

Revision ID: 25a7ccb31efd
Revises: 
Create Date: 2025-11-21 17:32:54.540156

"""
from alembic import op
import sqlalchemy as sa



revision = '25a7ccb31efd'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():

    op.create_table('posts',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=150), nullable=False),
    sa.Column('content', sa.Text(), nullable=False),
    sa.Column('posted', sa.DateTime(), nullable=False),
    sa.Column('category', sa.Enum('news', 'publication', 'tech', 'other', name='category_types'), nullable=True),
    sa.Column('is_active', sa.Boolean(), nullable=True),
    sa.Column('author', sa.String(length=20), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )


def downgrade():
    op.drop_table('posts')
