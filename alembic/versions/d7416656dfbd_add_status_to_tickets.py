"""add status to tickets

Revision ID: d7416656dfbd
Revises: 2e6991cebc16
Create Date: 2026-05-20 20:00:21.589461

"""

from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "d7416656dfbd"
down_revision: Union[str, Sequence[str], None] = "2e6991cebc16"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "tickets",
        sa.Column(
            "status",
            sa.String(),
            nullable=False,
            server_default="created",
        ),
    )

    op.execute("UPDATE tickets SET status = 'created' WHERE status IS NULL")

    op.alter_column(
        "tickets",
        "status",
        server_default=None,
    )


def downgrade() -> None:
    op.drop_column("tickets", "status")
