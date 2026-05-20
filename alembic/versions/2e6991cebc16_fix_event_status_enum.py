import sqlalchemy as sa

from alembic import op

revision = "2e6991cebc16"
down_revision = "ad9e40ba9775"

event_status_enum = sa.Enum(
    "new",
    "published",
    "registration_closed",
    "finished",
    name="eventstatus",
)


def upgrade() -> None:
    event_status_enum.create(op.get_bind(), checkfirst=True)

    op.alter_column(
        "events",
        "status",
        type_=event_status_enum,
        postgresql_using="status::text::eventstatus",
    )


def downgrade() -> None:
    op.alter_column(
        "events",
        "status",
        type_=sa.String(),
        postgresql_using="status::text",
    )

    event_status_enum.drop(op.get_bind(), checkfirst=True)
