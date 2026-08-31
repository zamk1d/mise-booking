from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from services.booking_service import BookingService
from src.database.db import get_db
from src.repository.booking_repository import BookingRepository


async def get_booking_repo(session: AsyncSession = Depends(get_db)) -> BookingRepository:
    return BookingRepository(session)

async def get_booking_service(repo: BookingRepository = Depends(get_booking_repo)) -> BookingService:
    return BookingService(repo)