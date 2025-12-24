from .db import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Integer, DateTime, Enum, ForeignKey, Text, Table, Column
from typing import Optional, List
from datetime import datetime, date
from enum import Enum as BoEnum

hotel_service = Table(
    'hotel_service',
    Base.metadata,
    Column('hotel_id', ForeignKey('hotel.id'), primary_key=True),
    Column('service_id', ForeignKey('service.id'), primary_key=True),
)


class StatusChoices(str, BoEnum):
    client = 'client'
    owner = 'owner'

class RoomType(str, BoEnum):
    lux = 'lux'
    economic = 'economic'
    family = 'family'
    one = 'one'

class RoomStatus(str, BoEnum):
    free = 'free'
    busy = 'busy'


class UserProfile(Base):
    __tablename__ = 'user_profile'
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    first_name: Mapped[str] = mapped_column(String(20))
    last_name: Mapped[str] = mapped_column(String(20))
    email: Mapped[str] = mapped_column(String(50), unique=True)
    password: Mapped[str] = mapped_column(String(50))
    username: Mapped[str] = mapped_column(String(50), unique=True)
    status: Mapped[StatusChoices] = mapped_column(String, Enum(StatusChoices), default=StatusChoices.client)
    user_image: Mapped[Optional[str]] = mapped_column(String)
    age: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    phone_number: Mapped[Optional[str]] = mapped_column(String)
    created_at: Mapped[date] = mapped_column(DateTime, default=datetime.today())
    user_country: Mapped[List['Country']] = relationship('Country', back_populates='user',
                                                         cascade='all, delete-orphan')
    user_hotel: Mapped[List['Hotel']] = relationship('Hotel' , back_populates='user',
                                                     cascade='all, delete-orphan')
    user_bookings: Mapped[List['Booking']] = relationship('Booking', back_populates='user',
                                                          cascade='all, delete-orphan')
    user_reviews: Mapped[List['Review']] = relationship('Review', back_populates='user',
                                                        cascade='all, delete-orphan')
    refresh_tokens: Mapped[List['RefreshToken']] = relationship(
        'RefreshToken',
        back_populates='user_token',
        cascade='all, delete-orphan'
    )


class Country(Base):
    __tablename__ = 'country'
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    country_name: Mapped[str] = mapped_column(String, unique=True)
    country_image: Mapped[Optional[str]] = mapped_column(String)
    user_id: Mapped[int] = mapped_column(ForeignKey('user_profile.id'))
    user: Mapped[UserProfile] = relationship(UserProfile, back_populates='user_country')
    hotel_country: Mapped[List['Hotel']] = relationship('Hotel', back_populates='country_hotel',
                                                        cascade='all, delete-orphan')


class City(Base):
    __tablename__ = 'city'
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    city_name: Mapped[str] = mapped_column(String, unique=True)
    city_image: Mapped[Optional[str]] = mapped_column(String)
    hotel_city: Mapped[List['Hotel']] = relationship('Hotel', back_populates='city',
                                                     cascade='all, delete-orphan')



class Service(Base):
    __tablename__ = 'service'
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    service_name: Mapped[str] = mapped_column(String)
    service_image: Mapped[Optional[str]] = mapped_column(String)
    hotels = relationship('Hotel',secondary=hotel_service,back_populates='services')

class Hotel(Base):
    __tablename__ = 'hotel'
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    hotel_name: Mapped[str] = mapped_column(String)
    city_id: Mapped[str] = mapped_column(ForeignKey('city.id'))
    city: Mapped[City] = relationship(City, back_populates='hotel_city')
    country_id: Mapped[int] = mapped_column(ForeignKey('country.id'))
    country_hotel: Mapped[Country] = relationship(Country, back_populates='hotel_country')
    hotel_stars: Mapped[Optional[int]] = mapped_column(Integer)
    street: Mapped[Optional[str]] = mapped_column(String(40))
    postal_index: Mapped[Optional[int]] = mapped_column(Integer)
    services = relationship('Service',secondary=hotel_service,back_populates='hotels')
    description: Mapped[Optional[str]] = mapped_column(Text)
    user_id: Mapped[int] = mapped_column(ForeignKey('user_profile.id'))
    user: Mapped[UserProfile] = relationship(UserProfile, back_populates='user_hotel')
    hotel_images: Mapped[List['HotelImage']] = relationship('HotelImage', back_populates='hotel',
                                                            cascade='all, delete-orphan')
    bookings: Mapped[List['Booking']] = relationship('Booking', back_populates='hotel',
                                                     cascade='all, delete-orphan')
    reviews: Mapped[List['Review']] = relationship('Review', back_populates='hotel',
                                                   cascade='all, delete-orphan')


class HotelImage(Base):
    __tablename__ = 'hotel_image'
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    hotel_id: Mapped[int] = mapped_column(ForeignKey('hotel.id'))
    hotel: Mapped[Hotel] = relationship(Hotel, back_populates='hotel_images')
    image_hotel: Mapped[Optional[str]] = mapped_column(String)



class Room(Base):
    __tablename__ = 'room'
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    room_number: Mapped[int] = mapped_column(Integer, unique=True)
    room_type: Mapped[RoomType] = mapped_column(String, Enum(RoomType), default=RoomType.economic)
    room_status: Mapped[RoomStatus] = mapped_column(String, Enum(RoomStatus), default=RoomStatus.free)
    room_description: Mapped[Optional[str]] = mapped_column(Text)
    price: Mapped[int] = mapped_column(Integer, nullable=False)
    room_images: Mapped[List['RoomImage']] = relationship('RoomImage', back_populates='room',
                                                                    cascade='all, delete-orphan')
    room_bookings: Mapped[List['Booking']] = relationship('Booking', back_populates='room',
                                                          cascade='all, delete-orphan')
class RoomImage(Base):
    __tablename__ = 'room_image'
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    room_id: Mapped[int] = mapped_column(ForeignKey('room.id'))
    room: Mapped[Room] = relationship(Room, back_populates='room_images')
    room_image: Mapped[str] = mapped_column(String, nullable=False)


class Booking(Base):
    __tablename__ = 'booking'
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    hotel_id: Mapped[int] = mapped_column(ForeignKey('hotel.id'))
    hotel: Mapped[Hotel] = relationship(Hotel, back_populates='bookings')
    room_id: Mapped[int] = mapped_column(ForeignKey('room.id'))
    room: Mapped[Room] = relationship(Room, back_populates='room_bookings')
    user_id: Mapped[int] = mapped_column(ForeignKey('user_profile.id'))
    user: Mapped[UserProfile] = relationship(UserProfile, back_populates='user_bookings')
    chek_in: Mapped[date] = mapped_column(DateTime, default=datetime.today())
    chek_out: Mapped[date] = mapped_column(DateTime, default=datetime.today())

class Review(Base):
    __tablename__ = 'review'
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    hotel_id: Mapped[int] = mapped_column(ForeignKey('hotel.id'))
    hotel: Mapped[Hotel] = relationship(Hotel, back_populates='reviews')
    user_id: Mapped[int] = mapped_column(ForeignKey('user_profile.id'))
    user: Mapped[UserProfile] = relationship(UserProfile, back_populates='user_reviews')
    commit: Mapped[Optional[str]] = mapped_column(Text)
    stars: Mapped[Optional[str]] = mapped_column(String(5))


class RefreshToken(Base):
    __tablename__ = 'refresh_token'
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('user_profile.id'))
    user_token: Mapped[UserProfile] = relationship(UserProfile, back_populates='refresh_tokens')
    token: Mapped[str] = mapped_column(String)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)



