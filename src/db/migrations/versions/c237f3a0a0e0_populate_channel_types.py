from typing import Sequence
from typing import Union

import sqlalchemy as sa
from alembic import op

from src.db.models.channel_type import ChannelTypeEnum
from src.db.models.channel_type import IntEnum

# revision identifiers, used by Alembic.
revision: str = "c237f3a0a0e0"
down_revision: Union[str, None] = "e97bbc0fdb6a"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:

    op.bulk_insert(
        sa.table(
            "channel_types",
            sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
            sa.Column("type", IntEnum(ChannelTypeEnum), nullable=False),
        ),
        [
            {"id": 1, "type": ChannelTypeEnum.YOUTUBE},
            {"id": 2, "type": ChannelTypeEnum.TWITCH},
        ],
    )


def downgrade() -> None:
    pass
