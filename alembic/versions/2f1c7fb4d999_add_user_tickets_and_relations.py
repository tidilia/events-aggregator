"""add user, tickets and relations

Revision ID: 2f1c7fb4d999
Revises: 192fc68d9ad3
Create Date: 2026-04-27 01:13:47.320670

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from datetime import datetime, timezone

# revision identifiers, used by Alembic.
revision: str = '2f1c7fb4d999'
down_revision: Union[str, Sequence[str], None] = '192fc68d9ad3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    # USERS
    op.create_table(
        "users",
        sa.Column("id", sa.String(), primary_key=True),
        sa.Column("first_name", sa.String(), nullable=False),
        sa.Column("last_name", sa.String(), nullable=False),
        sa.Column("email", sa.String(), nullable=False, unique=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            nullable=False,
            default=datetime.now(timezone.utc),
        ),
    )

    # TICKETS
    op.create_table(
        "tickets",
        sa.Column("id", sa.String(), primary_key=True),
        sa.Column("event_id", sa.String(), nullable=False),
        sa.Column("user_id", sa.String(), nullable=False),
        sa.Column("seat", sa.String(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            nullable=False,
            default=datetime.now(timezone.utc),
        ),
    )

    # FK tickets → events
    op.create_foreign_key(
        "fk_tickets_event",
        "tickets",
        "events",
        ["event_id"],
        ["id"],
    )

    # FK tickets → users
    op.create_foreign_key(
        "fk_tickets_user",
        "tickets",
        "users",
        ["user_id"],
        ["id"],
    )

    # UNIQUE seat per event
    op.create_unique_constraint(
        "uq_event_seat",
        "tickets",
        ["event_id", "seat"],
    )


def downgrade():
    op.drop_table("tickets")
    op.drop_table("users")