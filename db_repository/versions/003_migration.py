from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
target = Table('target', pre_meta,
    Column('id', INTEGER, primary_key=True, nullable=False),
    Column('name', VARCHAR(length=256)),
    Column('hostname', VARCHAR(length=120), nullable=False),
    Column('port', INTEGER),
    Column('sshoptions', VARCHAR(length=500)),
    Column('servertype', VARCHAR(length=64)),
    Column('autocommand', VARCHAR(length=128)),
    Column('comment', VARCHAR(length=500)),
)

target = Table('target', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('targetname', String(length=256)),
    Column('hostname', String(length=120), nullable=False),
    Column('port', Integer),
    Column('sshoptions', String(length=500)),
    Column('servertype', String(length=64)),
    Column('autocommand', String(length=128)),
    Column('comment', String(length=500)),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['target'].columns['name'].drop()
    post_meta.tables['target'].columns['targetname'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['target'].columns['name'].create()
    post_meta.tables['target'].columns['targetname'].drop()
