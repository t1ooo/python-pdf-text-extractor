from typing import Tuple
from app.celery_app import celery_app
from pdfminer.high_level import extract_text_to_fp


@celery_app.task(time_limit=20)
def extract_text_from_pdf(
    upload_filename: str, from_path: str, to_path: str
) -> Tuple[str, str]:
    with open(from_path, "rb") as f, open(to_path, "wb") as t:
        extract_text_to_fp(f, t)
    return (upload_filename, to_path)
