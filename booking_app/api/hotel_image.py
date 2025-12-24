from booking_app.database.models import HotelImage
from booking_app.database.schema import HotelImageInputSchema, HotelImageOutSchema
from booking_app.database.db import SessionLocal
from sqlalchemy.orm import Session
from typing import List
from fastapi import Depends, APIRouter, HTTPException

hotel_image_router = APIRouter(prefix='/hotel_image', tags=['Hotel_image'])
async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@hotel_image_router.post('/', response_model=HotelImageInputSchema)
async def create_hotel_image(hotel_image: HotelImageOutSchema, db: Session = Depends(get_db)):
    db_hotel_image = HotelImage(**hotel_image.dict())
    db.add(db_hotel_image)
    db.commit()
    db.refresh(db_hotel_image)
    return db_hotel_image

@hotel_image_router.get('/', response_model=List[HotelImageOutSchema])
async def get_all_hotel_images(db: Session = Depends(get_db)):
    image_db = db.query(HotelImage).all()
    return image_db

@hotel_image_router.get('/{image_id}', response_model=List[HotelImageOutSchema])
async def get_image(image_id: int, db: Session = Depends(get_db)):
    image_db = db.query(HotelImage).filter(HotelImage.id == image_id).first()
    if not image_db:
        raise HTTPException(status_code=400, detail='Image not found')
    return image_db


@hotel_image_router.put('/{image_id}', response_model=dict)
async def update_image(image_id: int, image: HotelImageOutSchema, db: Session = Depends(get_db)):
    image_db = db.query(HotelImage).filter(HotelImage.id == image_id).first()
    if not image_db:
        raise HTTPException(status_code=400, detail='Image not found')
    for image_key, image_value in image.dict().items():
        setattr(image_db, image_key, image_value)
    db.commit()
    db.refresh(image_db)
    return {'message': 'Image updated'
            }

@hotel_image_router.delete('/{image_id}', response_model=dict)
async def delete_image(image_id: int, db: Session = Depends(get_db)):
    image_db = db.query(HotelImage).filter(HotelImage.id == image_id).first()
    if not image_db:
        raise HTTPException(status_code=400, detail='Image not found')
    db.delete(image_db)
    db.commit()
    return {'message': 'Image deleted'}




