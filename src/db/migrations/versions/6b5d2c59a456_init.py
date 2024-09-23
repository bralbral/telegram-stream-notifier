"""init

Revision ID: 6b5d2c59a456
Revises: 
Create Date: 2024-09-23 12:13:56.930387

"""
from typing import Sequence
from typing import Union

import sqlalchemy as sa
import sqlmodel
from alembic import op

# revision identifiers, used by Alembic.
revision: str = '6b5d2c59a456'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('channel_types',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('type', sa.Enum('YOUTUBE', 'TWITCH', 'KICK', name='channeltype', length=15), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('type')
    )
    op.create_table('message_logs',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('message_id', sa.Integer(), nullable=False),
    sa.Column('text', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_message_logs_message_id'), 'message_logs', ['message_id'], unique=False)
    op.create_table('user_roles',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('role', sa.Enum('USER', 'SUPERUSER', 'UNKNOWN', name='userrole', length=15), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('role')
    )
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('username', sqlmodel.sql.sqltypes.AutoString(length=255), nullable=True),
    sa.Column('firstname', sqlmodel.sql.sqltypes.AutoString(length=255), nullable=True),
    sa.Column('lastname', sqlmodel.sql.sqltypes.AutoString(length=255), nullable=True),
    sa.Column('user_role_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_role_id'], ['user_roles.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_users_firstname'), 'users', ['firstname'], unique=False)
    op.create_index(op.f('ix_users_lastname'), 'users', ['lastname'], unique=False)
    op.create_index(op.f('ix_users_user_id'), 'users', ['user_id'], unique=True)
    op.create_index(op.f('ix_users_username'), 'users', ['username'], unique=False)
    op.create_table('channels',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('url', sqlmodel.sql.sqltypes.AutoString(length=255), nullable=False),
    sa.Column('label', sqlmodel.sql.sqltypes.AutoString(length=255), nullable=False),
    sa.Column('enabled', sa.Boolean(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('channel_type_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['channel_type_id'], ['channel_types.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_channels_enabled'), 'channels', ['enabled'], unique=False)
    op.create_index(op.f('ix_channels_label'), 'channels', ['label'], unique=False)
    op.create_index(op.f('ix_channels_url'), 'channels', ['url'], unique=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_channels_url'), table_name='channels')
    op.drop_index(op.f('ix_channels_label'), table_name='channels')
    op.drop_index(op.f('ix_channels_enabled'), table_name='channels')
    op.drop_table('channels')
    op.drop_index(op.f('ix_users_username'), table_name='users')
    op.drop_index(op.f('ix_users_user_id'), table_name='users')
    op.drop_index(op.f('ix_users_lastname'), table_name='users')
    op.drop_index(op.f('ix_users_firstname'), table_name='users')
    op.drop_table('users')
    op.drop_table('user_roles')
    op.drop_index(op.f('ix_message_logs_message_id'), table_name='message_logs')
    op.drop_table('message_logs')
    op.drop_table('channel_types')
    # ### end Alembic commands ###
