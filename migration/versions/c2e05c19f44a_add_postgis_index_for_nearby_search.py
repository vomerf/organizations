"""add postgis index for nearby search

Revision ID: c2e05c19f44a
Revises: f446d74c1717
Create Date: 2026-02-19 15:36:34.893057

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c2e05c19f44a'
down_revision: Union[str, Sequence[str], None] = 'f446d74c1717'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.execute("CREATE EXTENSION IF NOT EXISTS postgis;")
    op.execute(
        """
        CREATE INDEX IF NOT EXISTS ix_building_geo_geog
        ON building
        USING GIST (
            geography(ST_SetSRID(ST_MakePoint(longitude, latitude), 4326))
        );
        """
    )

def downgrade() -> None:
    """Downgrade schema."""
    op.execute("DROP INDEX IF EXISTS ix_building_geo_geog;")
