import uvicorn
from fastapi import FastAPI
from booking_app.api import users,hotel, country, city, service, hotel_image, room_image, auth, review, rooms
from booking_app.admin.setup import setup_admin

booking_app = FastAPI(title='Booking API')
booking_app.include_router(auth.auth_router)
booking_app.include_router(users.user_router)
booking_app.include_router(country.country_router)
booking_app.include_router(city.city_router)
booking_app.include_router(service.service_router)
booking_app.include_router(hotel_image.hotel_image_router)
booking_app.include_router(room_image.room_image_router)
booking_app.include_router(hotel.hotel_router)
booking_app.include_router(review.review_router)
booking_app.include_router(rooms.room_router)
setup_admin(booking_app)

if __name__ == '__main__':
    uvicorn.run(booking_app, host='127.0.0.1', port=8002)