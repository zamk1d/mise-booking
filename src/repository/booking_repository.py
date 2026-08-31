from datetime import date, time
from enum import Enum

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.models import Booking


class BookingRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get(self, booking_id: int) -> Booking | None:
        result = await self.session.execute(
            select(Booking).where(Booking.id == booking_id)
        )
        return result.scalar_one_or_none()

    async def get_by_datetime(self, booking_date: date, booking_time: time):
        result = await self.session.execute(
            select(Booking).where(
                Booking.booking_date == booking_date,
                Booking.booking_time == booking_time,
                Booking.status == Enum("active")
            )
        )
        return result.scalar_one_or_none()

    async def list(self, booking_date: date | None = None, limit: int = 50, offset: int = 0) -> list[Booking]:
        if booking_date is None:
            result = await self.session.execute(
                select(Booking).limit(limit).offset(offset)
            )
        else:
            result = await self.session.execute(
                select(Booking).where(Booking.booking_date == booking_date).limit(limit).offset(offset)
            )
        return list(result.scalars().all())

    async def create(self, **kwargs) -> Booking:
        booking = Booking(**kwargs)
        self.session.add(booking)
        await self.session.commit()
        return booking

    async def change_status(self, booking: Booking, status) -> Booking:
        booking.status = status
        await self.session.commit()
        return booking