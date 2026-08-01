"""add confirmed to orderstatus enum

Revision ID: f8c9d0e1f2a3
Revises: 2cad1a3d52a5
Create Date: 2026-07-31 00:00:00.000000
"""

from alembic import op

# revision identifiers, used by Alembic.
revision = 'f8c9d0e1f2a3'
down_revision = '6db7d9f7a4e1'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute("ALTER TYPE orderstatus ADD VALUE IF NOT EXISTS 'CONFIRMED'")


def downgrade() -> None:
    # PostgreSQL does not support removing enum values directly.
    pass
