from booking_app.database.models import Hotel
from booking_app.database.schema import HotelInputSchema, HotelOutSchema
from booking_app.database.db import SessionLocal
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

hotel_router = APIRouter(prefix='/hotel', tags=['Hotel'])
async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@hotel_router.post('/', response_model=HotelInputSchema)
async def post_hotel(hotel: HotelInputSchema, db: Session = Depends(get_db)):
    hotel_db = Hotel(**hotel.dict())
    db.add(hotel_db)
    db.commit()
    db.refresh(hotel_db)
    return hotel_db

@hotel_router.get('/', response_model=List[HotelOutSchema])
async def get_hotels(db: Session = Depends(get_db)):
    hotel_db = db.query(Hotel).all()
    return hotel_db

@hotel_router.get('/{hotel_id}', response_model=dict)
async def get_hotel(hotel_id: int, db: Session = Depends(get_db)):
    hotel_db = db.query(Hotel).filter(Hotel.id == hotel_id).first()
    if not hotel_db:
        raise HTTPException(status_code=404, detail='Hotel not found')
    return {'message' : 'Hotel found'}


@hotel_router.put('/{hotel_id}', response_model=dict)
async def upload_hotel(hotel_id: int, hotel: HotelOutSchema, db: Session = Depends(get_db)):
    hotel_db = db.query(Hotel).filter(Hotel.id == hotel).first()
    if not hotel_db:
        raise HTTPException(status_code=404, detail='Hotel not found')
    for hotel_key, hotel_value in hotel.dict().items():
        setattr(hotel_db, hotel_key, hotel_value)
    db.commit()
    db.refresh(hotel_db)
    return {'message' : 'Hotel updated'}

@hotel_router.delete('/{hotel_id}', response_model=dict)
async def delete_hotel(hotel_id: int, db: Session = Depends(get_db)):
    hotel_db = db.query(Hotel).filter(Hotel.id == hotel_id).first()
    if not hotel_db:
        raise HTTPException(status_code=404, detail='Hotel not delete ')
    db.delete(hotel_db)
    db.commit()
    return {'message' : 'категоря удалена '}


