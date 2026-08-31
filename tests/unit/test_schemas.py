from datetime import date, time, timedelta
import pytest
from freezegun import freeze_time
from pydantic import ValidationError
from src.schemas.booking import BookingCreate

def make_payload(**overrides):
    payload = {
        "name": "John Lenon",
        "phone": "89998765432",
        "guests_number": 2,
        "booking_date": date.today() + timedelta(days=5),
        "booking_time": time(14, 0)
    }
    payload.update(overrides)
    return payload

class TestBookingDateValidation:
    def test_valid_date_passes(self):
        booking = BookingCreate(**make_payload())
        assert booking.booking_date == make_payload()["booking_date"]

    def test_date_in_past_raises(self):
        with pytest.raises(ValidationError):
            BookingCreate(**make_payload(booking_date=date.today() - timedelta(days=1)))

    def test_date_90_days_passes(self):
        booking = BookingCreate(**make_payload(booking_date=date.today() + timedelta(days=90)))
        assert booking.booking_date == date.today() + timedelta(days=90)

    def test_date_91_days_raises(self):
        with pytest.raises(ValidationError):
            BookingCreate(**make_payload(booking_date=date.today() + timedelta(days=91)))

    def test_model_validator_returns_self(self):
        data = make_payload()
        booking = BookingCreate(**data)
        assert booking.booking_date == data["booking_date"]

class TestBookingTimeValidation:
    @pytest.mark.parametrize("hour", [12, 15, 22])
    def test_valid_hours_slots_passes(self, hour):
        booking = BookingCreate(**make_payload(booking_time=time(hour, 0)))
        assert booking.booking_time.hour == hour

    def test_non_hourly_slot_raises(self):
        with pytest.raises(ValidationError):
            BookingCreate(**make_payload(booking_time=time(12, 30)))

    @pytest.mark.parametrize("hour", [11, 23])
    def test_out_of_range_hour_raises(self, hour):
        with pytest.raises(ValidationError):
            BookingCreate(**make_payload(booking_time=time(hour, 0)))

class TestBookingDateTimeValidation:
    @freeze_time("2026-09-01 15:00:00")
    def test_booking_time_in_future_passes(self):
        booking = BookingCreate(
            **make_payload(
                booking_date=date(2026, 9, 1),
                booking_time=time(16, 0),
            )
        )

        assert booking.booking_date == date(2026, 9, 1)
        assert booking.booking_time == time(16, 0)

    @freeze_time("2026-09-01 15:00:00")
    def test_booking_time_in_past_raises(self):
        with pytest.raises(
            ValidationError,
            match="Cannot book a time slot in the past",
        ):
            BookingCreate(
                **make_payload(
                    booking_date=date(2026, 9, 1),
                    booking_time=time(14, 0),
                )
            )


class TestPhoneValidation:
    @pytest.mark.parametrize("phone", [
        "+79998765432",
        "89998765432",
        "+7-(999)-876-54-32"
    ])
    def test_valid_formats_passes(self, phone):
        booking = BookingCreate(**make_payload(phone=phone))
        assert booking.phone == phone

    @pytest.mark.parametrize("phone", [
        "123",
        "abc",
        "+19998765432"
    ])
    def test_invalid_formats_raises(self, phone):
        with pytest.raises(ValidationError):
            BookingCreate(**make_payload(phone=phone))

    def test_validate_phone_returns_value(self):
        assert BookingCreate.validate_phone("+79998765432") == "+79998765432"

class TestNameValidation:
    @pytest.mark.parametrize("name", [
        "John Lenon",
        "Anne-Mary",
        "Иван Петров"
    ])
    def test_valid_formats_passes(self, name):
        booking = BookingCreate(**make_payload(name=name))
        assert booking.name == name

    @pytest.mark.parametrize("name", [
        "123",
        "a_b!"
    ])
    def test_invalid_formats_raises(self, name):
        with pytest.raises(ValidationError):
            BookingCreate(**make_payload(name=name))