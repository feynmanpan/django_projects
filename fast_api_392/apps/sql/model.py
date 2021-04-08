from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
#
from .database import Base
##############################################################


class IPS(Base):
    __tablename__ = "ips"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)

    # items = relationship("Item", back_populates="owner")
