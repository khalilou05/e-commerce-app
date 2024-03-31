from pathlib import Path

from fastapi import UploadFile


async def article_img_upload(article_id: int, images: list[UploadFile]):
    path = Path() / "static"
    for index, image in enumerate(images):
        save_to = path / f"art_{article_id}_img_{index+1}.jpeg"
        img = await image.read()
        with open(save_to, "wb") as f:
            f.write(img)
