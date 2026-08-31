from sqlalchemy import String, Integer, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime

from src.repository.database.db import Base

class Booking(Base):
    __tablename__ = "bookings"

    id: Mapped[int] = mapped_column(Integer())
    name: Mapped[str] = mapped_column(String())
    phone: Mapped[int] = mapped_column(Integer())
    booking_date: Mapped[datetime] = mapped_column(DateTime())
    booking_time: Mapped[int] = mapped_column(Integer())
    guests_number: Mapped[int] = mapped_column(Integer())
    status: Mapped[str] = mapped_column(String())