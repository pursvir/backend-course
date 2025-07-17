import asyncio
import logging
import os

from PIL import Image

from src.db import async_session_maker_np
from src.tasks.celery_app import celery_instance
from src.utils.db_manager import DBManager

SIZES = (1000, 500, 200)
OUTPUT_FOLDER = "static/images"


@celery_instance.task
def resize_image(image_path: str):
    logging.debug(f"")
    img = Image.open(image_path)
    basename = os.path.basename(image_path)
    name, ext = os.path.splitext(basename)

    for size in SIZES:
        img_resized = img.resize(
            (size, int(img.height * (size / img.width))), Image.Resampling.LANCZOS
        )
        new_filename = f"{name}_{size}px{ext}"
        output_path = os.path.join(OUTPUT_FOLDER, new_filename)
        img_resized.save(output_path)

    logging.info(f"Image saved with following sizes: {SIZES} into the folder {OUTPUT_FOLDER}")


async def get_bookings_with_today_checkin_helper():
    async with DBManager(session_factory=async_session_maker_np) as db:
        bookings = await db.bookings.get_bookings_with_today_checkin()
        logging.debug(f"{bookings=}")


@celery_instance.task(name="booking_today_checkin")
def send_emails_to_users_with_today_checkin():
    asyncio.run(get_bookings_with_today_checkin_helper())
