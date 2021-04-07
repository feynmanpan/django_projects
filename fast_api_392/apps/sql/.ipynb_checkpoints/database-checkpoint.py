from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
##############################################################

SQLALCHEMY_DATABASE_URL = "postgresql://postgres:wtbcode@localhost/wtb"
#
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    # connect_args={"check_same_thread": False}, # 這個只有sqlite需要
)
#
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
#
Base = declarative_base()
