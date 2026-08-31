from datetime import date
from src.schemas.booking import BookingCreate, BookingStatus
from src.services.custom_exc import BookingNotFoundError, BookingAlreadyExistsError
from src.repository.booking_repository import BookingRepository


class BookingService:
    def __init__(self, repo: BookingRepository):
        self.repo = repo

    async def get_booking(self, booking_id: int):
        booking = await self.repo.get(booking_id)
        if booking is None:
            raise BookingNotFoundError(booking_id)
        return booking

    async def list_bookings(self, limit: int, offset: int, booking_date: date | None = None):
        return await self.repo.list(limit=limit, offset=offset, booking_date=booking_date)

    async def create_booking(self, data: BookingCreate):
        other_booking = await self.repo.get_by_datetime(booking_date=data.booking_date, booking_time=data.booking_time)
        if other_booking:
            raise BookingAlreadyExistsError((data.booking_date, data.booking_time))
        return await self.repo.create(**data.model_dump())

    async def change_status(self, booking_id: int, booking_status: BookingStatus):
        booking = await self.repo.get(booking_id=booking_id)
        if booking is None:
            raise BookingNotFoundError
        return await self.repo.change_status(booking=booking, status=booking_status)