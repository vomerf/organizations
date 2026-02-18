"""check constraint

Revision ID: f446d74c1717
Revises: 01010547b2b9
Create Date: 2026-02-10 10:47:29.244646

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f446d74c1717'
down_revision: Union[str, Sequence[str], None] = '01010547b2b9'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_check_constraint(
        "activity_level_check",
        "activity",
        "level BETWEEN 1 AND 3"
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint(
        "activity_level_check",
        "activity",
        type_="check"
    )