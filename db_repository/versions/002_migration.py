from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
group__group = Table('group__group', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('group_id', Integer),
    Column('containergroup_id', Integer),
)

target = Table('target', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('name', String(length=256)),
    Column('hostname', String(length=120), nullable=False),
    Column('port', Integer),
    Column('sshoptions', String(length=500)),
    Column('servertype', String(length=64)),
    Column('autocommand', String(length=128)),
    Column('comment', String(length=500)),
)

target__group = Table('target__group', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('target_id', Integer),
    Column('group_id', Integer),
)

target__t_group = Table('target__t_group', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('target_id', Integer),
    Column('tgroup_id', Integer),
)

targetgroup = Table('targetgroup', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('name', String(length=256)),
    Column('comment', String(length=500)),
)

tgroup__group = Table('tgroup__group', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('targetgroup_id', Integer),
    Column('group_id', Integer),
)

tgroup__tgroup = Table('tgroup__tgroup', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('targetgroup_id', Integer),
    Column('containertargetgroup_id', Integer),
)

user__group = Table('user__group', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('user_id', Integer),
    Column('group_id', Integer),
)

user__target = Table('user__target', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('user_id', Integer),
    Column('target_id', Integer),
)

usergroup = Table('usergroup', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('name', String(length=256)),
    Column('comment', String(length=500)),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['group__group'].create()
    post_meta.tables['target'].create()
    post_meta.tables['target__group'].create()
    post_meta.tables['target__t_group'].create()
    post_meta.tables['targetgroup'].create()
    post_meta.tables['tgroup__group'].create()
    post_meta.tables['tgroup__tgroup'].create()
    post_meta.tables['user__group'].create()
    post_meta.tables['user__target'].create()
    post_meta.tables['usergroup'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['group__group'].drop()
    post_meta.tables['target'].drop()
    post_meta.tables['target__group'].drop()
    post_meta.tables['target__t_group'].drop()
    post_meta.tables['targetgroup'].drop()
    post_meta.tables['tgroup__group'].drop()
    post_meta.tables['tgroup__tgroup'].drop()
    post_meta.tables['user__group'].drop()
    post_meta.tables['user__target'].drop()
    post_meta.tables['usergroup'].drop()
