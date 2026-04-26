"""add timezone to datetime fields

Revision ID: 192fc68d9ad3
Revises: ab93b174874b
Create Date: 2026-04-26 15:42:30.631230

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '192fc68d9ad3'
down_revision: Union[str, Sequence[str], None] = 'ab93b174874b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade():
    # events table
    op.alter_column(
        "events",
        "event_time",
        type_=sa.TIMESTAMP(timezone=True),
        postgresql_using="event_time AT TIME ZONE 'UTC'",
    )

    op.alter_column(
        "events",
        "registration_deadline",
        type_=sa.TIMESTAMP(timezone=True),
        postgresql_using="registration_deadline AT TIME ZONE 'UTC'",
    )

    op.alter_column(
        "events",
        "changed_at",
        type_=sa.TIMESTAMP(timezone=True),
        postgresql_using="changed_at AT TIME ZONE 'UTC'",
    )

    op.alter_column(
        "events",
        "created_at",
        type_=sa.TIMESTAMP(timezone=True),
        postgresql_using="created_at AT TIME ZONE 'UTC'",
    )

    op.alter_column(
        "events",
        "status_changed_at",
        type_=sa.TIMESTAMP(timezone=True),
        postgresql_using="status_changed_at AT TIME ZONE 'UTC'",
    )

    op.alter_column(
        "events",
        "place_changed_at",
        type_=sa.TIMESTAMP(timezone=True),
        postgresql_using="place_changed_at AT TIME ZONE 'UTC'",
    )

    op.alter_column(
        "events",
        "place_created_at",
        type_=sa.TIMESTAMP(timezone=True),
        postgresql_using="place_created_at AT TIME ZONE 'UTC'",
    )
    
    op.alter_column(
        "sync_metadata",
        "last_sync_time",
        type_=sa.TIMESTAMP(timezone=True),
        postgresql_using="last_sync_time AT TIME ZONE 'UTC'",
    )

    op.alter_column(
        "sync_metadata",
        "last_changed_at",
        type_=sa.TIMESTAMP(timezone=True),
        postgresql_using="last_changed_at AT TIME ZONE 'UTC'",
    )


def downgrade():
    op.alter_column("events", "event_time", type_=sa.TIMESTAMP(timezone=False))
    op.alter_column("events", "registration_deadline", type_=sa.TIMESTAMP(timezone=False))
    op.alter_column("events", "changed_at", type_=sa.TIMESTAMP(timezone=False))
    op.alter_column("events", "created_at", type_=sa.TIMESTAMP(timezone=False))
    op.alter_column("events", "status_changed_at", type_=sa.TIMESTAMP(timezone=False))
    op.alter_column("events", "place_changed_at", type_=sa.TIMESTAMP(timezone=False))
    op.alter_column("events", "place_created_at", type_=sa.TIMESTAMP(timezone=False))
    op.alter_column(
        "sync_metadata",
        "last_sync_time",
        type_=sa.TIMESTAMP(timezone=False),
        postgresql_using="last_sync_time AT TIME ZONE 'UTC'",
    )

    op.alter_column(
        "sync_metadata",
        "last_changed_at",
        type_=sa.TIMESTAMP(timezone=False),
        postgresql_using="last_changed_at AT TIME ZONE 'UTC'",
    )