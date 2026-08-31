import re
from datetime import date, time, timedelta, datetime
from enum import Enum

from pydantic import BaseModel, Field, ConfigDict, field_validator, model_validator


class BookingStatus(str, Enum):
    active = "active"
    cancelled = "canceled"

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

    @field_validator("booking_time")
    @classmethod
    def validate_booking_time(cls, value: time) -> time:
        if value.minute != 0 or value.second != 0:
            raise ValueError("Only hourly slots are allowed")
        if value.hour not in range(12, 22):
            raise ValueError("Only reservation between 12:00 and 23:00 is allowed")
        return value

class BookingResponse(BookingCreate):
    model_config = ConfigDict(from_attributes=True)

    id: int
    status: BookingStatus

class BookingUpdate(BaseModel):
    status: BookingStatus