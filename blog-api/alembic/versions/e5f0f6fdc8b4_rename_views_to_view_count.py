"""rename views to view_count

Revision ID: e5f0f6fdc8b4
Revises: 0386858a74cb
Create Date: 2026-10-23 16:16:13.620171

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e5f0f6fdc8b4'
down_revision: Union[str, Sequence[str], None] = '0386858a74cb'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Rename views to view_count, data ke saath."""
    op.alter_column("blogs", "views", new_column_name="view_count")


def downgrade() -> None:
    """Wapas view_count to views."""
    op.alter_column("blogs", "view_count", new_column_name="views")
