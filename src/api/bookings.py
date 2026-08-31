from fastapi import APIRouter

api = APIRouter()

@api.post("/bookings", status_code=201)
async def create_booking():
    return {"status": "ok"}

@api.get("/bookings", status_code=200)
async def get_bookings():
    return {"status": "ok"}

@api.get("/bookings/{id}", status_code=200)
async def get_booking(id: int):
    return {"status": "ok"}

@api.delete("/bookings/{id}", status_code=200)
async def delete_booking(id: int):
    return {"status": "ok"}