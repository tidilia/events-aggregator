"""revert event status enum

Revision ID: 7ced37215057
Revises: 9e1d1fb2cc2a
Create Date: 2026-05-13 23:03:19.971134

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "7ced37215057"
down_revision: Union[str, Sequence[str], None] = "9e1d1fb2cc2a"
branch_labels = None
depends_on = None


ENUM_NAME = "eventstatus"


def upgrade() -> None:
    # enum -> varchar
    op.alter_column(
        "events",
        "status",
        type_=sa.String(),
        existing_type=sa.Enum(name=ENUM_NAME),
        postgresql_using="status::text",
        nullable=False,
    )

    # удалить enum type из postgres
    op.execute(f"DROP TYPE IF EXISTS {ENUM_NAME}")


def downgrade() -> None:
    # recreate enum
    event_status = sa.Enum(
        "DRAFT",
        "PUBLISHED",
        "FINISHED",
        "CANCELLED",
        "REGISTRATION_CLOSED",
        name=ENUM_NAME,
    )

    event_status.create(op.get_bind(), checkfirst=True)

    op.alter_column(
        "events",
        "status",
        type_=event_status,
        existing_type=sa.String(),
        postgresql_using=f"status::text::{ENUM_NAME}",
        nullable=False,
    )