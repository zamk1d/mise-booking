from datetime import date, time, timedelta
from unittest.mock import AsyncMock
import pytest
from src.repository.booking_repository import BookingRepository
from src.schemas.booking import BookingCreate, BookingStatus
from src.services.booking_service import BookingService
from src.services.custom_exc import BookingNotFoundError, BookingAlreadyExistsError

@pytest.fixture
def mock_repo():
    return AsyncMock(spec=BookingRepository)

@pytest.fixture
def service(mock_repo):
    return BookingService(mock_repo)

class TestCreateBooking:
    async def test_creates_when_slot_free(self, service, mock_repo):
        mock_repo.get_by_datetime.return_value = None
        mock_repo.create.return_value = "object"

        data = BookingCreate(
            name="John Lenon",
            phone="+79998765432",
            guests_number=2,
            booking_date=date.today() + timedelta(days=1),
            booking_time=time(14, 0)
        )

        result = await service.create_booking(data)
        mock_repo.get_by_datetime.assert_awaited_once_with(
            booking_date=data.booking_date, booking_time=data.booking_time
        )
        mock_repo.create.assert_awaited_once()
        assert result == "object"

    async def test_raises_when_slot_taken(self, service, mock_repo):
        mock_repo.get_by_datetime.return_value = "existing_object"

        data = BookingCreate(
            name="John Lenon",
            phone="+79998765432",
            guests_number=2,
            booking_date=date.today() + timedelta(days=1),
            booking_time=time(14, 0)
        )

        with pytest.raises(BookingAlreadyExistsError):
            await service.create_booking(data)

        mock_repo.create.assert_not_awaited()

class TestGetBooking:
    async def test_returns_booking_when_found(self, service, mock_repo):
        mock_repo.get.return_value = "object"
        result = await service.get_booking(booking_id=1)
        assert result == "object"

    async def test_raises_when_not_found(self, service, mock_repo):
        mock_repo.get.return_value = None
        with pytest.raises(BookingNotFoundError):
            await service.get_booking(booking_id=999)

    async def test_change_status_raises_when_not_found(self, service, mock_repo):
        mock_repo.get.return_value = None
        service = BookingService(mock_repo)
        with pytest.raises(BookingNotFoundError):
            await service.change_status(booking_id=123, booking_status=BookingStatus.canceled)
        mock_repo.get.assert_awaited_once_with(booking_id=123)