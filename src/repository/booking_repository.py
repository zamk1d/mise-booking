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

    async def list(self, limit: int = 50, offset: int = 0) -> list[Booking]:
        result = await self.session.execute(
            select(Booking).limit(limit).offset(offset)
        )
        return list(result.scalars().all())

    async def create(self, **kwargs) -> Booking:
        booking = Booking(**kwargs)
        self.session.add(booking)
        await self.session.commit()
        return booking

    async def delete(self, booking: Booking) -> None:
        await self.session.delete(booking)