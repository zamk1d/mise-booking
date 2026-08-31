import re
from datetime import date, time, timedelta, datetime
from enum import Enum

from pydantic import BaseModel, Field, ConfigDict, field_validator, model_validator


class BookingStatus(str, Enum):
    active = "active"
    cancelled = "cancelled"

class BookingBase(BaseModel):
    name: str = Field(min_length=2)
    phone: str
    guests: int = Field(ge=1, le=12)

    @field_validator("phone")
    @classmethod
    def validate_phone(cls, value: str) -> str:
        digits = re.sub(r"\D", "", value)
        if len(digits) == 11 and digits[0] in ("7", "8"):
            return value
        raise ValueError(
            "Enter valid number: +7 or 8, 10 digits"
        )

class BookingCreate(BookingBase):
    booking_date: date
    booking_time: time

    @field_validator("booking_date")
    @classmethod
    def validate_booking_date(cls, value: date) -> date:
        today = date.today()
        max_date = today + timedelta(days=90)

        if value < today:
            raise ValueError("Booking date cannot be in the past")
        if value > max_date:
            raise ValueError("Only booking in the 90 days is allowed")
        return value

class BookingResponse(BookingCreate):
    model_config = ConfigDict(from_attributes=True)

    id: int
    status: BookingStatus

class BookingUpdate(BaseModel):
    status: BookingStatus