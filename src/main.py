#!/usr/bin/env python3

from fastapi import FastAPI, Request
import uvicorn
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from src.api.hotels import router as hotels_router
from src.config import settings
# from src.db import ...

print(f"{settings.DB_URL=}")

app = FastAPI()
app.include_router(hotels_router)

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
