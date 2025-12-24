from booking_app.database.models import (UserProfile, Country, City, Service,
                                         Hotel, HotelImage, Room, RoomImage,
                                         Booking, Review,
                                         RefreshToken)
from sqladmin import ModelView

class UserProfileAdmin(ModelView, model=UserProfile):
    column_list = [UserProfile.first_name, UserProfile.last_name]


class CountryAdmin(ModelView, model=Country):
    column_list = [Country.country_name, Country.country_image]

class CityAdmin(ModelView, model=City):
    column_list = [City.city_name, City.city_image]

class ServiceAdmin(ModelView, model=Service):
    column_list = [Service.service_name, Service.service_image]

class HotelAdmin(ModelView, model=Hotel):
    column_list = [Hotel.hotel_name, Hotel.hotel_images]


class HotelImageAdmin(ModelView, model=HotelImage):
    column_list = [HotelImage.image_hotel]

class RoomAdmin(ModelView, model=Room):
    column_list = [Room.room_number, Room.room_description]


class RoomImageAdmin(ModelView, model=RoomImage):
    column_list = [RoomImage.room_image]

