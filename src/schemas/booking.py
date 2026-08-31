import re
from datetime import date, time, timedelta, datetime
from enum import Enum

from pydantic import BaseModel, Field, ConfigDict, field_validator, model_validator


class BookingStatus(str, Enum):
    active = "active"
    cancelled = "canceled"

class BookingBase(BaseModel):
    name: str = Field(
        min_length=2,
        description="Your name",
        examples=["John"]
    )
    phone: str = Field(
        description="Your phone number",
        examples=["+79998765432", "+7-(999)-876-54-32", "89998765432"]
    )
    guests_number: int = Field(
        ge=1,
        le=12,
        description="Number of guests you planning to come. Maximum - 12",
        examples=["1", "2"]
    )

    @field_validator("name")
    @classmethod
    def validate_name(cls, value: str) -> str:
        if not re.fullmatch(r"[A-Za-zA-Яя-Ёё\s\-]+", value):
            raise ValueError("Name must be only leters, spaces and hyphens")
        return value

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
    booking_date: date = Field(
        description="A date when you planning to come",
        examples=["2026-12-01"]
    )
    booking_time: time = Field(
        description="A time when you planning to come, only hourly slots available",
        examples=["12:00", "13:00", "23:00"]
    )

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
        if value.hour not in range(12, 23):
            raise ValueError("Only reservation between 12:00 and 23:00 is allowed")
        return value

    @model_validator(mode="after")
    def validate_datetime_together(self) -> "BookingCreate":
        booking_datetime = datetime.combine(self.booking_date, self.booking_time)
        if booking_datetime < datetime.now():
            raise ValueError("Cannot book a time slot in the past")
        return self

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "name": "John Lenon",
                "phone": "+79998765432",
                "guests_number": 2,
                "booking_date": "2026-09-15",
                "booking_time": "18:00"
            }
        }
    )

class BookingResponse(BookingCreate):
    model_config = ConfigDict(from_attributes=True)

    id: int
    status: BookingStatus

class BookingUpdate(BaseModel):
    status: BookingStatus