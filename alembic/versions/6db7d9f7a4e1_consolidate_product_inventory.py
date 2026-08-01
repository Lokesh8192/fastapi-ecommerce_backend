"""consolidate product inventory into stock_quantity

Revision ID: 6db7d9f7a4e1
Revises: 315935a49356
Create Date: 2026-07-31

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "6db7d9f7a4e1"
down_revision: Union[str, Sequence[str], None] = "315935a49356"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Preserve the previously used stock values, then remove the duplicate column."""
    op.execute("UPDATE products SET stock_quantity = stock")
    op.drop_column("products", "stock")


def downgrade() -> None:
    """Restore the legacy stock column from the inventory source of truth."""
    op.add_column(
        "products",
        sa.Column("stock", sa.Integer(), nullable=False, server_default="0"),
    )
    op.execute("UPDATE products SET stock = stock_quantity")
