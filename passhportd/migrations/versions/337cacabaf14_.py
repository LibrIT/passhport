"""empty message

Revision ID: 337cacabaf14
Revises: dec7b631ea28
Create Date: 2018-06-08 21:44:18.166327

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '337cacabaf14'
down_revision = 'dec7b631ea28'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('logentry', sa.Column('endsessiondate', sa.String(length=20), nullable=True))
    op.create_index(op.f('ix_logentry_endsessiondate'), 'logentry', ['endsessiondate'], unique=False)
    op.add_column('target', sa.Column('changepwd', sa.Boolean(), nullable=True))
    op.add_column('target', sa.Column('deleted', sa.Boolean(), nullable=True))
    op.add_column('target', sa.Column('sessiondur', sa.Integer(), nullable=True))
    op.create_index(op.f('ix_target_changepwd'), 'target', ['changepwd'], unique=False)
    op.create_index(op.f('ix_target_sessiondur'), 'target', ['sessiondur'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_target_sessiondur'), table_name='target')
    op.drop_index(op.f('ix_target_changepwd'), table_name='target')
    op.drop_column('target', 'sessiondur')
    op.drop_column('target', 'deleted')
    op.drop_column('target', 'changepwd')
    op.drop_index(op.f('ix_logentry_endsessiondate'), table_name='logentry')
    op.drop_column('logentry', 'endsessiondate')
    # ### end Alembic commands ###