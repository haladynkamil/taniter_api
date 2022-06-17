from .database import Base
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Date, Float
from sqlalchemy.orm import relationship
from sqlalchemy.schema import UniqueConstraint
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    results = relationship("Result", back_populates="owner")


class Result(Base):
    __tablename__ = "results"

    id = Column(Integer, primary_key=True, index=True)
    owner_id = Column(Integer, ForeignKey("users.id"))
    date = Column(Date)
    weight = Column(Float)
    bodyfat = Column(Float)
    muscle_mass = Column(Float)
    water_weight = Column(Float)
    metabolic_age = Column(Integer)
    intestines_fat = Column(Integer)
    kcal = Column(Integer)
    owner = relationship("User", back_populates="results")
    __table_args__ = (UniqueConstraint('date', 'owner_id', name='uix_1'),)
