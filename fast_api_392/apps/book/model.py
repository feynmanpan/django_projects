from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
#
from apps.sql.config import Base


##############################################################
class INFO(Base):
    __tablename__ = "info"
    #
    idx = Column(Integer, primary_key=True, autoincrement=True)
    #
    store = Column(String, nullable=True)
    bookid = Column(String, nullable=True)
    isbn10 = Column(String, nullable=True)
    isbn13 = Column(String, nullable=True)
    title = Column(String, nullable=True)
    title2 = Column(String, nullable=True)
    author = Column(String, nullable=True)
    publisher = Column(String, nullable=True)
    pub_dt = Column(String, nullable=True)
    lang = Column(String, nullable=True)
