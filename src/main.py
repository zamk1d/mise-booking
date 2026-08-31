import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from src.services.custom_exc import BookingNotFoundError, BookingAlreadyExistsError
from src.api.bookings import api
from src.core.log_config import setup_logging

logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    setup_logging()
    yield
    logger.info("Shutdown")

app = FastAPI(title="mise-booking", lifespan=lifespan)
app.include_router(api)

@app.exception_handler(BookingNotFoundError)
async def booking_not_found_handler(request: Request, exc: BookingNotFoundError):
    logger.warning("Booking not found: %s", exc)
    return JSONResponse(status_code=404, content={"detail": "Booking not found"})

@app.exception_handler(BookingAlreadyExistsError)
async def booking_already_exists_handler(request: Request, exc: BookingAlreadyExistsError):
    logger.warning("Booking slot already booked: %s", exc)
    return JSONResponse(status_code=409, content={"detail": "This time slot is already booked"})