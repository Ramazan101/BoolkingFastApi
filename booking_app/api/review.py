from booking_app.database.models import Review
from booking_app.database.schema import ReviewInputSchema, ReviewOutSchema
from booking_app.database.db import SessionLocal
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, APIRouter
from typing import List


review_router = APIRouter(prefix='/review', tags=['Review'])
async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@review_router.post('/', response_model=ReviewOutSchema)
async def review_create(review: ReviewInputSchema,  db: Session = Depends(get_db)):
    review_db = Review(**review.dict())
    db.add(review_db)
    db.commit()
    db.refresh(review_db)
    return review_db

@review_router.get('/', response_model=List[ReviewOutSchema])
async def get_reviews(db: Session = Depends(get_db)):
    return db.query(Review).all()


@review_router.get('/{review_id}', response_model=ReviewOutSchema)
async def get_review_by_id(review_id: int, db: Session = Depends(get_db)):
    review_db = db.query(Review).filter(Review.id == review_id).first()
    if not review_db:
        raise HTTPException(status_code=404, detail='Review not found')
    return review_db


@review_router.put('/{review_id}', response_model=dict)
async def update_review(review_id: int, review: ReviewInputSchema, db: Session = Depends(get_db)):
    db_review = db.query(Review).filter(Review.id == review_id).first()
    if not db_review:
        raise HTTPException(status_code=404, detail='Review not found')
    for review_key, review_value in review.dict().items():
        setattr(db_review, review_key, review_value)
    db.commit()
    db.refresh(db_review)
    return {'message': 'Review updated'}



@review_router.delete('/{review_id}', response_model=dict)
async def delete_review(review_id: int, db: Session = Depends(get_db)):
    db_review = db.query(Review).filter(Review.id == review_id).first()
    if not db_review:
        raise HTTPException(status_code=404, detail='Review not found')
    db.delete(db_review)
    db.commit()
    return {'message': 'Review deleted'}

