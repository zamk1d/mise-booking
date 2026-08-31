from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.api.bookings import api

app = FastAPI(title="mise-booking")
app.include_router(api)
@app.get("/")
async def root():
    return {"status": "ok"}