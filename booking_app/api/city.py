from booking_app.database.models import City
from booking_app.database.schema import CityInputSchema, CityOutSchema
from booking_app.database.db import SessionLocal
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

city_router = APIRouter(prefix='/city', tags=['City'])
async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@city_router.post('/', response_model=CityInputSchema)
async def create_city(city: CityOutSchema, db: Session = Depends(get_db)):
    city_db = City(**city.dict())
    db.add(city_db)
    db.commit()
    db.refresh(city_db)
    return city_db


@city_router.get('/', response_model=List[CityInputSchema])
async def get_city(db: Session = Depends(get_db)):
    city_db = db.query(City).all()
    return city_db

@city_router.get('/{city_id}', response_model=CityInputSchema)
async def get_city_id(city_id: int, db: Session = Depends(get_db)):
    city_db = db.query(City).filter(City.id == city_id).first()
    if not city_db:
        raise HTTPException(status_code=404, detail='City not found')
    return city_db

@city_router.put('/{city_id}', response_model=dict)
async def update_city(city_id: int, city: CityInputSchema, db: Session = Depends(get_db)):
    city_db = db.query(City).filter(City.id == city_id).first()
    if not city_db:
        raise HTTPException(status_code=400, detail='City not found')
    for city_key, city_value in city.dict().items():
        setattr(city_db, city_key, city_value)
    db.commit()
    db.refresh(city_db)
    return {'message': 'City updated'}


@city_router.delete('/{city_id}', response_model=dict)
async def delete_city(city_id: int, db: Session = Depends(get_db)):
    city_db = db.query(City).filter(City.id == city_id).first()
    if not city_db:
        raise HTTPException(status_code=400, detail='city not delete')
    db.delete(city_db)
    db.commit()
    return {'message': 'City deleted'}




