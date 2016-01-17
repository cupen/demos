from collections import OrderedDict

from sqlalchemy import create_engine, MetaData, Table, Integer, String, Column
from sqlalchemy.orm import Session

def create_testdb(database, reCreate=False):
    dbfile = database + '.db'
    import os
    if os.path.exists(dbfile):
        return create_engine('sqlite:///%s'%dbfile)

    meta = MetaData()
    tables = OrderedDict()
    tables['human'] = Table('human', meta,
        Column('id', Integer, primary_key=True),
        Column('name', String(60), nullable=False),
        Column('level', Integer, nullable=False)
    )
    tables['monster'] = Table('monster', meta,
        Column('id', Integer, primary_key=True),
        Column('name', String(60), nullable=False),
        Column('level', Integer, nullable=False)
    )

    engine = create_engine('sqlite:///%s'%dbfile)
    meta.create_all(engine, checkfirst=True)

    conn = engine.connect()
    for i in range(100):
        conn.execute(tables['human'].insert(), id=i, name='human_%s'%i, level=i)
        conn.execute(tables['monster'].insert(), id=i, name='monster%s'%i, level=i)
    return engine