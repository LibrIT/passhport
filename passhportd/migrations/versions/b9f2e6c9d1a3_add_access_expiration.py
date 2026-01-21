"""add access expiration

Revision ID: b9f2e6c9d1a3
Revises: 13746bb16d7b
Create Date: 2025-01-21 00:00:00.000000
"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b9f2e6c9d1a3'
down_revision = '13746bb16d7b'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('target_user', sa.Column('expires_at', sa.DateTime(), nullable=True))
    op.create_index(op.f('ix_target_user_expires_at'), 'target_user', ['expires_at'], unique=False)
    op.add_column('target_group', sa.Column('expires_at', sa.DateTime(), nullable=True))
    op.create_index(op.f('ix_target_group_expires_at'), 'target_group', ['expires_at'], unique=False)
    op.add_column('tgroup_user', sa.Column('expires_at', sa.DateTime(), nullable=True))
    op.create_index(op.f('ix_tgroup_user_expires_at'), 'tgroup_user', ['expires_at'], unique=False)
    op.add_column('tgroup_group', sa.Column('expires_at', sa.DateTime(), nullable=True))
    op.create_index(op.f('ix_tgroup_group_expires_at'), 'tgroup_group', ['expires_at'], unique=False)


def downgrade():
    op.drop_index(op.f('ix_tgroup_group_expires_at'), table_name='tgroup_group')
    op.drop_column('tgroup_group', 'expires_at')
    op.drop_index(op.f('ix_tgroup_user_expires_at'), table_name='tgroup_user')
    op.drop_column('tgroup_user', 'expires_at')
    op.drop_index(op.f('ix_target_group_expires_at'), table_name='target_group')
    op.drop_column('target_group', 'expires_at')
    op.drop_index(op.f('ix_target_user_expires_at'), table_name='target_user')
    op.drop_column('target_user', 'expires_at')
