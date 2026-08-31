import pytest
from datetime import date, time, timedelta
from src.repository.booking_repository import BookingRepository
from src.schemas.booking import BookingStatus

def valid_data(**override):
    data = {
        "name": "John Lenon",
        "phone": "+79998765432",
        "booking_date": date.today() + timedelta(days=1),
        "booking_time": time(14, 0),
        "guests_number": 2,
    }
    data.update(override)
    return data

class TestBookingRepository:
    async def test_create_and_get_booking(self, db_session):
        repo = BookingRepository(db_session)
        created = await repo.create(**valid_data())
        assert created.id is not None
        fetched = await repo.get(created.id)
        assert fetched is not None
        assert fetched.id == created.id
        assert fetched.name == "John Lenon"

    async def test_get_by_datetime_found(self, db_session):
        repo = BookingRepository(db_session)
        booking_date = date.today() + timedelta(days=2)
        booking_time = time(15, 0)
        await repo.create(**valid_data(booking_date=booking_date, booking_time=booking_time))
        found = await repo.get_by_datetime(booking_date=booking_date, booking_time=booking_time)
        assert found is not None
        assert found.booking_date == booking_date
        assert found.booking_time == booking_time

    async def test_get_by_datetime_not_found(self, db_session):
        repo = BookingRepository(db_session)
        found = await repo.get_by_datetime(date.today() + timedelta(days=10), time(10, 0))
        assert found is None

    async def test_list_without_date(self, db_session):
        repo = BookingRepository(db_session)
        for i in range(10):
            booking = valid_data(name=f"User {i}")
            await repo.create(**booking)
        results = await repo.list(limit=10, offset=0)
        assert len(results) >= 10

    async def test_list_with_date(self, db_session):
        repo = BookingRepository(db_session)
        target_date = date.today() + timedelta(days=5)
        booking = valid_data(booking_date=target_date)
        await repo.create(**booking)
        another_booking = valid_data(booking_date=date.today() + timedelta(days=6))
        await repo.create(**another_booking)
        results = await repo.list(booking_date=target_date, limit=10, offset=0)
        assert len(results) == 1
        assert results[0].booking_date == target_date

    async def test_change_status(self, db_session):
        repo = BookingRepository(db_session)
        created = await repo.create(**valid_data())
        updated = await repo.change_status(created, BookingStatus.canceled)
        assert updated.status == BookingStatus.canceled
        fetched = await repo.get(created.id)
        assert fetched.status == BookingStatus.canceled

