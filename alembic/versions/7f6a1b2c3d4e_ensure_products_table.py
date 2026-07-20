"""ensure products table exists

Revision ID: 7f6a1b2c3d4e
Revises: e9ce1f8489fb
Create Date: 2026-07-20 17:25:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = '7f6a1b2c3d4e'
down_revision: Union[str, Sequence[str], None] = 'e9ce1f8489fb'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    bind = op.get_bind()
    inspector = sa.inspect(bind)

    if inspector.has_table('products'):
        return

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
    bind = op.get_bind()
    inspector = sa.inspect(bind)

    if not inspector.has_table('products'):
        return

    op.drop_constraint('fk_products_created_by_users', 'products', type_='foreignkey')
    op.drop_constraint('fk_products_category_id_categories', 'products', type_='foreignkey')
    op.drop_table('products')
