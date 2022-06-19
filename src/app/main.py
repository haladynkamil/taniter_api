import pydantic.error_wrappers
from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
from fastapi.datastructures import UploadFile
from . import crud, models, schemas
from .database import SessionLocal, engine
from fastapi.param_functions import File
import datetime
import pandas as pd
import io
models.Base.metadata.create_all(bind=engine)
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.exc import IntegrityError

app = FastAPI()
origins = ['http://localhost:3001', 'http://localhost:3000']
app.add_middleware(CORSMiddleware, allow_origins=origins, allow_credentials=True, allow_methods=['*'], allow_headers=['*'])

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/users", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)


@app.get("/users", response_model=list[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users


@app.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@app.post("/users/{user_id}/results", status_code=201)
def create_results_for_user(
    user_id: int, db: Session = Depends(get_db), fileobject: UploadFile = File(...),
):

    results = str(fileobject.file.read().decode())
    for result in results.splitlines():
        result = result.split(',')
        result_dict = {
            'date': datetime.datetime.strptime(result[13], '%d/%m/%Y').date(), 'weight': result[27], 'bodyfat': result[31], 'muscle_mass': result[43],
            'water_weight': result[63], 'metabolic_age': result[61], 'intestines_fat': result[57], 'kcal': result[59]
        }
        try:
            result = schemas.ResultCreate(**result_dict)
        except:
            continue
        user_results = crud.get_results_by_user(db, user_id=user_id, date=result_dict['date'])
        if result and not user_results:
            try:
                crud.create_user_item(db=db, result=result, user_id=user_id)
            except pydantic.error_wrappers.ValidationError:
                pass
    return 0


@app.get("/results/", response_model=list[schemas.Result])
def read_results(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    results = crud.get_items(db, skip=skip, limit=limit)
    return results
