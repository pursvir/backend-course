#!/usr/bin/env python3

import logging
import sys
from contextlib import asynccontextmanager
from pathlib import Path

import uvicorn
from fastapi import FastAPI
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend

logging.basicConfig(level=logging.INFO)

sys.path.append(str(Path(__file__).parent.parent))

from src.api.auth import router as auth_router
from src.api.bookings import router as bookings_router
from src.api.facilities import router as facilities_router
from src.api.hotels import router as hotels_router
from src.api.images import router as images_router
from src.api.rooms import router as rooms_router
from src.init import redis_manager


@asynccontextmanager
async def lifespan(app: FastAPI):
    await redis_manager.connect()
    FastAPICache.init(backend=RedisBackend(redis_manager._redis), prefix="fastapi-cache")
    logging.info("FastAPI cache initialized")
    yield
    await redis_manager.close()


app = FastAPI(lifespan=lifespan)
app.include_router(auth_router)
app.include_router(hotels_router)
app.include_router(rooms_router)
app.include_router(bookings_router)
app.include_router(facilities_router)
app.include_router(images_router)

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
