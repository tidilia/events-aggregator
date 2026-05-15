"""add cascade delete for outbox ticket fk

Revision ID: ad9e40ba9775
Revises: 491809a995e9
Create Date: 2026-05-15 13:57:33.650132

"""
from typing import Sequence, Union

from alembic import op

# revision identifiers, used by Alembic.
revision: str = 'ad9e40ba9775'
down_revision: Union[str, Sequence[str], None] = '491809a995e9'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.drop_constraint(
        "fk_outbox_ticket",
        "outbox",
        type_="foreignkey"
    )

    op.create_foreign_key(
        "fk_outbox_ticket",
        "outbox",
        "tickets",
        ["ticket_id"],
        ["id"],
        ondelete="CASCADE"
    )


def downgrade() -> None:
    op.drop_constraint(
        "fk_outbox_ticket",
        "outbox",
        type_="foreignkey"
    )

    op.create_foreign_key(
        "fk_outbox_ticket",
        "outbox",
        "tickets",
        ["ticket_id"],
        ["id"]
    )