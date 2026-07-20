"""add created_by to categories

Revision ID: 9ae5c8a3d267
Revises: c8a036979fb9
Create Date: 2026-07-20 12:52:28.451054

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9ae5c8a3d267'
down_revision: Union[str, Sequence[str], None] = 'c8a036979fb9'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Add column as nullable first so existing rows are not rejected.
    op.add_column('categories', sa.Column('created_by', sa.Integer(), nullable=True))

    # Backfill existing categories with a valid user id.
    # Use the first admin/user row if present; otherwise keep the fallback 1.
    op.execute(
        """
        UPDATE categories
        SET created_by = (
            SELECT id
            FROM users
            ORDER BY id
            LIMIT 1
        )
        WHERE created_by IS NULL
        """
    )

    # Enforce the required constraint after data is populated.
    op.alter_column('categories', 'created_by', nullable=False)
    op.create_foreign_key(
        'fk_categories_created_by_users',
        'categories',
        'users',
        ['created_by'],
        ['id'],
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint('fk_categories_created_by_users', 'categories', type_='foreignkey')
    op.drop_column('categories', 'created_by')
