from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker, declarative_base

engine = create_engine(
    "postgresql+psycopg2://postgres.qibjoqedmynvzantnlkj:8UMWs7XOA4q7AkUZ@aws-0-us-west-1.pooler.supabase.com:5432/postgres",
)
db_session = scoped_session(
    sessionmaker(autocommit=False, autoflush=False, bind=engine)
)

Base = declarative_base()
Base.query = db_session.query_property()


def init_db():
    import src.models

    Base.metadata.create_all(bind=engine)
