from datetime import date, timedelta

import pytest

from src.schemas.booking import BookingResponse, BookingStatus


def valid_payload(**override):
    payload = {
        "name": "John Lenon",
        "phone": "+79998765432",
        "guests_number": 2,
        "booking_date": str(date.today() + timedelta(days=5)),
        "booking_time": "14:00:00",
    }
    payload.update(override)
    return payload

class TestCreateBooking:
    async def test_create_returns_201_with_active_status(self, client):
        response = await client.post("/bookings/", json=valid_payload())
        assert response.status_code == 201
        body = response.json()
        assert body["status"] == "active"
        assert "id" in body
        scheme = BookingResponse.model_validate(body)
        assert scheme.name == "John Lenon"
        assert scheme.status == BookingStatus.active

    async def test_create_with_invalid_phone_returns_422(self, client):
        response = await client.post("/bookings/", json=valid_payload(phone="123"))
        assert response.status_code == 422

    async def test_duplicate_slot_returns_409(self, client):
        payload = valid_payload()
        first_response = await client.post("/bookings/", json=payload)
        assert first_response.status_code == 201
        second_response = await client.post("/bookings/", json=payload)
        assert second_response.status_code == 409
        assert second_response.json() == {"detail": "This time slot is already booked"}

    async def test_same_date_different_time_succeeds(self, client):
        payload = valid_payload()
        await client.post("/bookings/", json=payload)
        other_payload = valid_payload(booking_time="15:00")
        response = await client.post("/bookings/", json=other_payload)
        assert response.status_code == 201

class TestGetBooking:
    async def test_get_existing_booking(self, client):
        create_resp = await client.post("/bookings/", json=valid_payload())
        booking_id = create_resp.json()["id"]
        response = await client.get(f"/bookings/{booking_id}")
        assert response.status_code == 200
        assert response.json()["id"] == booking_id
        scheme = BookingResponse.model_validate(response.json())
        assert scheme.name == "John Lenon"
        assert scheme.status == BookingStatus.active

    async def test_get_not_existing_booking_returns_404(self, client):
        response = await client.get("/bookings/123")
        assert response.status_code == 404
        assert response.json() == {"detail": "Booking not found"}

class TestListBookings:
    async def test_empty_list_when_no_bookings(self, client):
        response = await client.get("/bookings/")
        assert response.status_code == 200
        assert response.json() == []

    async def test_filter_by_date(self, client):
        dates = [str(date.today() + timedelta(days=day)) for day in range(5, 6)]
        for test_date in dates:
            await client.post("/bookings/", json=valid_payload(booking_date=test_date))
        response = await client.get(f"/bookings/?bookings_date={dates[0]}")
        assert response.status_code == 200
        results = response.json()
        assert len(results) == 1
        assert results[0]["booking_date"] == dates[0]
        schemes = [BookingResponse.model_validate(item) for item in response.json()]
        assert len(schemes) == 1
        assert schemes[0].booking_date == date.fromisoformat(dates[0])

class TestDeleteBooking:
    async def test_delete_sets_status_canceled(self, client):
        create_resp = await client.post("/bookings/", json=valid_payload())
        booking_id = create_resp.json()["id"]
        response = await client.delete(f"/bookings/{booking_id}")
        assert response.status_code == 200
        assert response.json()["status"] == "canceled"
        body = response.json()
        scheme = BookingResponse.model_validate(body)
        assert scheme.name == "John Lenon"
        assert scheme.status == BookingStatus.canceled

    async def test_delete_not_existing_returns_404(self, client):
        response = await client.delete("/bookings/123")
        assert response.status_code == 404
        assert response.json() == {"detail": "Booking not found"}