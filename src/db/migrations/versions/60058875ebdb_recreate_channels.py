from typing import Sequence
from typing import Union

import sqlalchemy as sa
from alembic import op

from src.db.models.channel_type import ChannelTypeEnum

# revision identifiers, used by Alembic.
revision: str = "60058875ebdb"
down_revision: Union[str, None] = "c237f3a0a0e0"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:

    try:
        with op.batch_alter_table("channels", schema=None) as batch_op:
            batch_op.drop_index("ix_channels_enabled")
            batch_op.drop_index("ix_channels_label")
            batch_op.drop_index("ix_channels_url")
    except:
        pass

    op.create_table(
        "channels_new",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("url", sa.String(length=255), nullable=False),
        sa.Column("label", sa.String(length=255), nullable=False),
        sa.Column("enabled", sa.Boolean(), nullable=True),
        sa.Column("created_at", sa.TIMESTAMP(), nullable=False),
        sa.Column("updated_at", sa.TIMESTAMP(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column(
            "channel_type_id",
            sa.Integer(),
            nullable=False,
            server_default=str(ChannelTypeEnum.YOUTUBE),
        ),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["users.id"],
            onupdate="CASCADE",
            ondelete="CASCADE",
            name="fk_channels_user_id",
        ),
        sa.ForeignKeyConstraint(
            ["channel_type_id"],
            ["channel_types.id"],
            onupdate="CASCADE",
            ondelete="CASCADE",
            name="fk_channels_channel_type_id",
        ),
        sa.PrimaryKeyConstraint("id", name="pk"),
        sa.UniqueConstraint("url", name="ix_uniq_url"),
    )
    op.create_index(
        op.f("ix_channels_enabled"), "channels_new", ["enabled"], unique=False
    )
    op.create_index(op.f("ix_channels_label"), "channels_new", ["label"], unique=False)
    op.create_index(op.f("ix_channels_url"), "channels_new", ["url"], unique=False)

    op.execute(
        """
                INSERT INTO channels_new
                SELECT *
                FROM channels
            """
    )

    op.drop_table("channels")
    op.execute("ALTER TABLE channels_new RENAME TO channels")


def downgrade() -> None:
    pass
