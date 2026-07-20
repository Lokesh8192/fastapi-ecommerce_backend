"""create products table

Revision ID: e9ce1f8489fb
Revises: 9ae5c8a3d267
Create Date: 2026-07-20 16:27:47.459174

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e9ce1f8489fb'
down_revision: Union[str, Sequence[str], None] = '9ae5c8a3d267'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        'products',
        sa.Column('id', sa.Integer(), primary_key=True, nullable=False),
        sa.Column('description', sa.Text(), nullable=False),
        sa.Column('price', sa.Numeric(precision=10, scale=2), nullable=False),
        sa.Column('stock', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('image_url', sa.String(length=500), nullable=True),
        sa.Column('category_id', sa.Integer(), nullable=False),
        sa.Column('created_by', sa.Integer(), nullable=False),
        sa.Column('is_active', sa.Boolean(), nullable=False, server_default=sa.text('true')),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('NOW()')),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('NOW()')),
    )
    op.create_foreign_key(
        'fk_products_category_id_categories',
        'products',
        'categories',
        ['category_id'],
        ['id'],
    )
    op.create_foreign_key(
        'fk_products_created_by_users',
        'products',
        'users',
        ['created_by'],
        ['id'],
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint('fk_products_created_by_users', 'products', type_='foreignkey')
    op.drop_constraint('fk_products_category_id_categories', 'products', type_='foreignkey')
    op.drop_table('products')
