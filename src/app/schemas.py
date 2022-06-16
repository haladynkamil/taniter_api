from typing import Union
from datetime import date
from pydantic import BaseModel


class ResultBase(BaseModel):
    date: date
    weight: float
    bodyfat: float
    muscle_mass: float
    water_weight: float
    metabolic_age: int
    intestines_fat: int
    kcal: int


class ResultCreate(ResultBase):
    pass


class Result(ResultBase):
    id: int
    owner_id: int

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    email: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    results: list[Result] = []

    class Config:
        orm_mode = True
