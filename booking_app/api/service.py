from booking_app.database.models import Service
from booking_app.database.schema import ServiceInputSchema, ServiceOutSchema
from booking_app.database.db import SessionLocal
from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

service_router = APIRouter(prefix='/service', tags=['Service'])
async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@service_router.post('/', response_model=ServiceInputSchema)
async def get_services(service: ServiceOutSchema, db: Session = Depends(get_db)):
    service_db = Service(**service.dict())
    db.add(service_db)
    db.commit()
    db.refresh(service_db)
    return service_db

@service_router.get('/', response_model=List[ServiceInputSchema])
async def get_services(db: Session = Depends(get_db)):
    service_db = db.query(Service).all()
    return service_db




@service_router.get('/{service_id}', response_model=List[ServiceInputSchema])
async def get_service(service_id: int, db: Session = Depends(get_db)):
    service_db = db.query(Service).filter(Service.id == service_id).first()
    if not service_db:
        raise HTTPException(status_code=404, detail='Service not found')
    return service_db

@service_router.put('/{service_id}', response_model=dict)
async def update_service(service_id: int, service: ServiceInputSchema, db: Session = Depends(get_db)):
    service_db = db.query(Service).filter(Service.id == service_id).first()
    if not service_db:
        raise HTTPException(status_code=400, detail='Service not found')
    for service_key, service_value in service.dict().items():
        setattr(service_db, service_key, service_value)
    db.commit()
    db.refresh(service_db)
    return {'messege': 'Service updated'}


@service_router.delete('/{service_id}', response_model=dict)
async def delete_service(service_id: int, db: Session = Depends(get_db)):
    service_db = db.query(Service).filter(Service.id == service_id).first()
    if not service_db:
        raise HTTPException(status_code=404, detail='Service not found')
    db.delete(service_db)
    db.commit()
    return {'message': 'Service deleted'}
