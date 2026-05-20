"""add idempotency_key to tickets

Revision ID: 491809a995e9
Revises: d343f55561f8
Create Date: 2026-05-14 15:36:13.651342
"""

import sqlalchemy as sa

from alembic import op

revision = "491809a995e9"
down_revision = "d343f55561f8"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("tickets", sa.Column("idempotency_key", sa.String(), nullable=True))

    op.create_unique_constraint(
        "uq_tickets_idempotency_key", "tickets", ["idempotency_key"]
    )


def downgrade() -> None:
    op.drop_constraint("uq_tickets_idempotency_key", "tickets", type_="unique")

    op.drop_column("tickets", "idempotency_key")
