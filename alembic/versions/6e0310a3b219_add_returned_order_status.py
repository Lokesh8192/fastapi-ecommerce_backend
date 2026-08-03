"""add returned order status

Revision ID: 6e0310a3b219
Revises: 1934c52da16d
Create Date: 2026-08-03 15:35:26.850042

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6e0310a3b219'
down_revision: Union[str, Sequence[str], None] = '1934c52da16d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Add the new RETURNED value to the existing PostgreSQL enum type.
    op.execute("ALTER TYPE orderstatus ADD VALUE IF NOT EXISTS 'RETURNED'")


def downgrade() -> None:
    """Downgrade schema."""
    # PostgreSQL does not support removing enum values safely.
    # This downgrade is intentionally left empty.
    pass
