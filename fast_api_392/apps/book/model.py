from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
#
from apps.sql.config import Base


##############################################################
class INFO(Base):
    __tablename__ = "info"
    #
    id = Column(Integer, primary_key=True, autoincrement=True)
    #
    title = Column(String, nullable=False)
    title2 = Column(String, nullable=False)
