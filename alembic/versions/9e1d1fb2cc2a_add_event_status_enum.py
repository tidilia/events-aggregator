"""add event status enum

Revision ID: 9e1d1fb2cc2a
Revises: 2f1c7fb4d999
Create Date: 2026-05-13 14:34:08.731972
"""

from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

# revision identifiers
revision: str = "9e1d1fb2cc2a"
down_revision: Union[str, Sequence[str], None] = "2f1c7fb4d999"
branch_labels = None
depends_on = None


ENUM_NAME = "eventstatus"


def upgrade() -> None:
    # 1. создаём enum тип в БД
    event_status = sa.Enum(
        "new",
        "published",
        "registration_closed",
        "finished",
        name=ENUM_NAME,
    )
    event_status.create(op.get_bind(), checkfirst=True)

    # 2. меняем колонку status
    op.alter_column(
        "events",
        "status",
        type_=event_status,
        existing_type=sa.VARCHAR(),
        postgresql_using="status::text::eventstatus",
        nullable=False,
    )


def downgrade() -> None:
    # откатываем обратно в VARCHAR
    op.alter_column(
        "events",
        "status",
        type_=sa.VARCHAR(),
        existing_type=sa.Enum(name=ENUM_NAME),
        postgresql_using="status::text",
        nullable=False,
    )

    # удаляем enum тип
    event_status = sa.Enum(name=ENUM_NAME)
    event_status.drop(op.get_bind(), checkfirst=True)
