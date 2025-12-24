from typing import Optional
from .models import StatusChoices, RoomType, RoomStatus
from pydantic import BaseModel,EmailStr
from datetime import date, datetime

class UserProfileInputSchema(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    password: str
    username: str
    status: StatusChoices
    user_image: Optional[str]
    age: Optional[int]
    phone_number: Optional[str]
    created_at: datetime

class UserProfileOutSchema(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: EmailStr
    password: str
    username: str
    status: StatusChoices
    user_image: Optional[str]
    age: Optional[int]
    phone_number: Optional[str]
    created_at: datetime


class UserRegisterSchema(BaseModel):
    username: str
    password: str

class CountryInputSchema(BaseModel):
    country_name: str
    country_image: Optional[str]
    user_id: int

class CountryOutSchema(BaseModel):
    id: int
    country_name: str
    country_image: Optional[str]
    user_id: int


class CityInputSchema(BaseModel):
    city_name: str
    city_image: Optional[str]

class CityOutSchema(BaseModel):
    id: int
    city_name: str
    city_image: Optional[str]

class ServiceInputSchema(BaseModel):
    service_name: str
    service_image: Optional[str]

class ServiceOutSchema(BaseModel):
    id: int
    service_name: str
    service_image: Optional[str]

class HotelInputSchema(BaseModel):
    hotel_name: str
    city_id: str
    country_id: int
    hotel_stars: int
    street: Optional[str]
    postal_index: Optional[str]
    destination: Optional[str]
    user_id: int


class HotelOutSchema(BaseModel):
    id: int
    hotel_name: str
    city_id: str
    country_id: int
    hotel_stars: int
    street: Optional[str]
    postal_index: Optional[str]
    destination: Optional[str]
    user_id: int


class HotelImageInputSchema(BaseModel):
    id: int
    hotel_id: int

class HotelImageOutSchema(BaseModel):
    hotel_id: int

class RoomInputSchema(BaseModel):
    room_number: int
    room_type: RoomType
    room_status: RoomStatus
    room_description: Optional[str]
    price: str

class RoomOutSchema(BaseModel):
    room_number: int
    room_type: RoomType
    room_status: RoomStatus
    room_description: Optional[str]
    price: str

class RoomImageInputSchema(BaseModel):
    room_id: int
    room_image: str


class RoomImageOutSchema(BaseModel):
    id: int
    room_id: int
    room_image: str

class BookingInputSchema(BaseModel):
    hotel_id: int
    room_id: int
    user_id: int
    chek_in: datetime
    chek_out: datetime


class BookingOutSchema(BaseModel):
    id: int
    hotel_id: int
    room_id: int
    user_id: int
    chek_in: datetime
    chek_out: datetime

class ReviewInputSchema(BaseModel):
    id: int
    hotel_id: int
    user_id: int
    commit: Optional[str]
    stars: Optional[str]

class ReviewOutSchema(BaseModel):
    id: int
    hotel_id: int
    user_id: int
    commit: Optional[str]
    stars: Optional[str]



