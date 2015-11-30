# -*- coding: utf-8 -*-
"""Setting up SQLAlchemy for querying."""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker

Base = declarative_base()
engine = create_engine('postgresql://r2c2:r2c2@localhost/r2c2',
                       convert_unicode=True, client_encoding='utf8')
db_session = session = scoped_session(sessionmaker(autocommit=False,
                                                   autoflush=False,
                                                   bind=engine))

Base.query = db_session.query_property()
