from booking_app.database.models import Room
from booking_app.database.schema import RoomInputSchema, RoomOutSchema
from booking_app.database.db import SessionLocal
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

room_router = APIRouter(prefix='/rooms', tags=['Rooms'])
async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@room_router.post('/', response_model=RoomInputSchema)
async def get_room(room: RoomOutSchema,  db: Session = Depends(get_db)):
    room_db = Room(**room.dict())
    db.add(room_db)
    db.commit()
    db.refresh(room_db)
    return room_db

@room_router.get('/', response_model=List[RoomOutSchema])
async def get_room(db: Session = Depends(get_db)):
    db_room = db.query(Room).all()
    return db_room

@room_router.get('/{room_id}', response_model=RoomOutSchema)
async def room_get(room_id: int, db: Session = Depends(get_db)):
    room_db = db.query(Room).filter(Room.id == room_id).first()
    if not room_db:
        raise HTTPException(status_code=404, detail="Room not found")
    return room_db


@room_router.put('/{room_id}', response_model=dict)
async def update_app(room_id: int, room: RoomOutSchema, db: Session = Depends(get_db)):
    room_db = db.query(Room).filter(Room.id == room_id).first()
    if not room_db:
        raise HTTPException(status_code=404, detail="Room not found")
    for room_key, room_value in room.dict().items():
        setattr(room_db, room_key, room_value)
    db.commit()
    db.refresh(room_db)
    return {'message': 'Room updated'}


@room_router.delete('/{room_id}', response_model=dict)
async def delete_room(room_id: int, db: Session = Depends(get_db)):
    room_db = db.query(Room).filter(Room.id == room_id).first()
    if not room_db:
        raise HTTPException(status_code=404, detail="Room not found")
    db.delete(room_db)
    db.commit()
    return {'message': 'Room deleted'}

