from sqlalchemy import String, Integer, Enum, Date, Time
from sqlalchemy.orm import Mapped, mapped_column
from datetime import date, time

from schemas.booking import BookingStatus
from database.db import Base

class Booking(Base):
    __tablename__ = "bookings"

    id: Mapped[int] = mapped_column(Integer(), primary_key=True)
    name: Mapped[str] = mapped_column(String())
    phone: Mapped[str] = mapped_column(String())
    booking_date: Mapped[date] = mapped_column(Date())
    booking_time: Mapped[time] = mapped_column(Time())
    guests_number: Mapped[int] = mapped_column(Integer())
    status: Mapped[str] = mapped_column(Enum(BookingStatus), default=BookingStatus.active)