import os
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker, scoped_session

Base = declarative_base()

_engine = None
_session_factory = sessionmaker(autocommit=False, autoflush=False)
db_session = scoped_session(_session_factory)

def init_db_engine(db_uri=None):
    global _engine
    if db_uri is None:
        db_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'instance', 'student_performance.db'))
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        db_uri = f'sqlite:///{db_path}'

    _engine = create_engine(db_uri, echo=False, connect_args={"check_same_thread": False})
    _session_factory.configure(bind=_engine)
    return _engine

def get_engine():
    global _engine
    if _engine is None:
        init_db_engine()
    return _engine

def get_session():
    if _engine is None:
        init_db_engine()
    return db_session
