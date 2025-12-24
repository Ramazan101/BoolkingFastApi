from booking_app.database.models import RoomImage
from booking_app.database.schema import RoomImageInputSchema, RoomImageOutSchema
from booking_app.database.db import SessionLocal
from sqlalchemy.orm import Session
from typing import List
from fastapi import Depends, APIRouter, HTTPException


room_image_router = APIRouter(prefix='/room_images', tags=['Rooms Images'])
async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



@room_image_router.post('/',response_model=RoomImageOutSchema)
async def create_room_image(room_image: RoomImageInputSchema, db: Session = Depends(get_db)):
    room_image_db = RoomImage(**room_image.dict())
    db.add(room_image_db)
    db.commit()
    db.refresh(room_image_db)
    return room_image_db

@room_image_router.get('/',response_model=List[RoomImageOutSchema])
async def get_images(db: Session = Depends(get_db)):
    return db.query(RoomImage).all()

@room_image_router.get('/{room_image_id}',response_model=RoomImageOutSchema)
async def get_image(room_image_id: int, db: Session = Depends(get_db)):
    room_image_db = db.query(RoomImage).filter(RoomImage.id == room_image_id).first()
    if not room_image_db:
        raise HTTPException(status_code=404, detail="Room not found")
    return room_image_db


@room_image_router.put('/{room_image_id}',response_model=RoomImageOutSchema)
async def update_image(room_image_id: int, room_image: RoomImageInputSchema, db: Session = Depends(get_db)):
    image_db = db.query(RoomImage).filter(RoomImage.id == room_image_id).first()
    if not image_db:
        raise HTTPException(status_code=404, detail="Room not found")
    for image_key, image_value in room_image.dict().items():
        setattr(image_db, image_key, image_value)

    db.commit()
    db.refresh(image_db)
    return {'message' : 'Room image updated'

            }


@room_image_router.delete('/{room_image_id}', response_model=dict)
async def delete_image(room_image_id: int, db: Session = Depends(get_db)):
    image_db = db.query(RoomImage).filter(RoomImage.id == room_image_id).first()
    if not image_db:
        raise HTTPException(status_code=404, detail="Room not found")
    db.delete(image_db)
    db.commit()
    return {'message' : 'Room image deleted'

            }