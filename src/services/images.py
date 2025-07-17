import shutil

from fastapi import UploadFile

IMAGES_DIR = "static/images"


class ImagesService:
    def add_image(self, file: UploadFile):
        image_path = f"{IMAGES_DIR}/{file.filename}"
        with open(image_path, "wb+") as img:
            shutil.copyfileobj(file.file, img)
            resize_image.delay(image_path)  # type: ignore
