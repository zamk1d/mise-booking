from enum import Enum

from fastapi import APIRouter, Body, Depends, HTTPException
from typing import Annotated
from datetime import date

from schemas.booking import BookingStatus
from services.custom_exc import BookingNotFoundError
from src.api.depends import get_booking_service
from src.services.booking_service import BookingService
from src.schemas.booking import BookingResponse, BookingCreate

api = APIRouter(prefix="bookings", tags=["bookings"])

@api.post("/", status_code=201, response_model=BookingResponse)
async def create_booking(
        data: Annotated[BookingCreate, Body()],
        service: BookingService = Depends(get_booking_service)
) -> BookingResponse:
    """creates new booking after validation and checking accessibility for booking"""
    created_booking = await service.create_booking(data)
    return BookingResponse(**created_booking)

@api.get("/", status_code=200, response_model=list[BookingResponse])
async def get_bookings(
        limit: int = 50,
        offset: int = 0,
        bookings_date: date | None = None,
        service: BookingService = Depends(get_booking_service)
) -> BookingResponse:
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
    try:
        booking = await service.get_booking(
            booking_id=booking_id
        )
    except BookingNotFoundError:
        raise HTTPException(status_code=404, detail="Booking not found")

    return BookingResponse(**booking)

@api.delete("/{booking_id}", status_code=204)
async def delete_booking(
        booking_id: int,
        service: BookingService = Depends(get_booking_service)
):
    """changes status of a booking from 'active' to 'canceled'"""
    await service.change_status(booking_id=booking_id, booking_status=BookingStatus.cancelled)
