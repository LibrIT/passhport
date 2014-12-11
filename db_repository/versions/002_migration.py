from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
user = Table('user', pre_meta,
    Column('id', INTEGER, primary_key=True, nullable=False),
    Column('name', VARCHAR(length=256)),
    Column('email', VARCHAR(length=120), nullable=False),
    Column('sshkey', VARCHAR(length=500), nullable=False),
    Column('comment', VARCHAR(length=500)),
)

user = Table('user', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('username', String(length=256)),
    Column('email', String(length=120), nullable=False),
    Column('sshkey', String(length=500), nullable=False),
    Column('comment', String(length=500)),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['user'].columns['name'].drop()
    post_meta.tables['user'].columns['username'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['user'].columns['name'].create()
    post_meta.tables['user'].columns['username'].drop()
