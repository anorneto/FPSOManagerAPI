from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
import datetime

from api.database import Base

class Vessel(Base):
    __tablename__ = "vessels"

    id = Column(Integer, primary_key=True, index=True)
    code = Column(String, unique=True, index=True, nullable=False)
    is_active = Column(Boolean, index=True, default=True)

    create_date = Column(DateTime, default=datetime.datetime.now)
    update_date = Column(DateTime, onupdate=datetime.datetime.now)
    delete_date = Column(DateTime)

    equipments = relationship("Equipment", back_populates="owner")
