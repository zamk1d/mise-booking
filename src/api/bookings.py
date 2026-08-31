from enum import Enum

from fastapi import APIRouter, Body, Depends, Query
from typing import Annotated
from datetime import date

from src.schemas.booking import BookingStatus
from src.services.custom_exc import BookingNotFoundError
from src.api.depends import get_booking_service
from src.services.booking_service import BookingService
from src.schemas.booking import BookingResponse, BookingCreate

api = APIRouter(prefix="/bookings", tags=["bookings"])

@api.post("/", status_code=201, response_model=BookingResponse)
async def create_booking(
        data: Annotated[BookingCreate, Body()],
        service: BookingService = Depends(get_booking_service)
) -> BookingResponse:
    """creates new booking after validation and checking accessibility for booking"""
    created_booking = await service.create_booking(data)
    return BookingResponse.model_validate(created_booking)

@api.get("/", status_code=200, response_model=list[BookingResponse])
async def get_bookings(
        limit: int = Query(default=50, ge=1, le=100, description="Max number of bookings to return"),
        offset: int = Query(default=0, ge=0, description="Number of bookings to skip"),
        bookings_date: date | None = None,
        service: BookingService = Depends(get_booking_service)
) -> list[BookingResponse]:
    """returns list of a books with pagination and filtration by date opportunity"""
    bookings_list = await service.list_bookings(
        limit=limit,
        offset=offset,
        booking_date=bookings_date
    )
    return bookings_list

@api.get("/{booking_id}", status_code=200, response_model=BookingResponse)
async def get_booking(
        booking_id: int,
        service: BookingService = Depends(get_booking_service)
) -> BookingResponse:
    """returns booking by id"""
    booking = await service.get_booking(
        booking_id=booking_id
    )

    return BookingResponse.model_validate(booking)

@api.delete("/{booking_id}", status_code=200, response_model=BookingResponse)
async def delete_booking(
        booking_id: int,
        service: BookingService = Depends(get_booking_service)
)-> BookingResponse:
    """changes status of a booking from 'active' to 'canceled'"""
    booking = await service.change_status(booking_id=booking_id, booking_status=BookingStatus.cancelled)
    return BookingResponse.model_validate(booking)