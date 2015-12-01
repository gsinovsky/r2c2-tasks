# -*- coding: utf-8 -*-
"""Setting up SQLAlchemy for querying."""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker

Base = declarative_base()
#Uncomment for local connection
#engine = create_engine('postgresql://r2c2:r2c2@localhost/r2c2',
#                      convert_unicode=True, client_encoding='utf8')
#Remote connection
username = 'postgres'
password = 'postgres'
server = '159.90.8.39'
engine = create_engine('postgresql://%s:%s@%s' %(username,password,server),
                       convert_unicode=True, client_encoding='utf8')
db_session = session = scoped_session(sessionmaker(autocommit=False,
                                                   autoflush=False,
                                                   bind=engine))
Base.query = db_session.query_property()