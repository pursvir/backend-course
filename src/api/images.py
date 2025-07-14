import shutil
from fastapi import APIRouter, UploadFile

from src.tasks.tasks import resize_image

router = APIRouter(prefix="/images", tags=["Изображения отелей"])


@router.post("")
def upload_image(file: UploadFile) -> None:
    image_path = f"static/images/{file.filename}"
    with open(image_path, "wb+") as img:
        shutil.copyfileobj(file.file, img)
    resize_image.delay(image_path) # type: ignore
