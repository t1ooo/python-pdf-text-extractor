import enum
import uuid
import logging
import os
import tempfile
from typing import BinaryIO, Optional, Tuple
import magic
from app.celery_app import is_celery_started, task_result
from app.celery_tasks import extract_text_from_pdf


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class PdfExtractorException(Exception):
    pass


def gen_uuid() -> str:
    return str(uuid.uuid4())


def is_pdf_file(f: BinaryIO) -> bool:
    return magic.from_descriptor(f.fileno()).startswith("PDF document")


_TEMPDIR = os.path.join(tempfile.gettempdir(), "python-pdf-text-extractor")


def upload_pdf(upload_filename: str, file: BinaryIO) -> str:
    if not is_pdf_file(file):
        raise PdfExtractorException("Not a pdf file.")

    id = gen_uuid()
    from_path = os.path.join(_TEMPDIR, f"{id}.pdf")
    to_path = os.path.join(_TEMPDIR, f"{id}.txt")

    os.makedirs(_TEMPDIR, exist_ok=True)
    with open(from_path, "wb") as f:
        f.write(file.read())

    extract_text_from_pdf.apply_async((upload_filename, from_path, to_path), task_id=id)
    return id


class Status(str, enum.Enum):
    IN_PROGRESS = "IN_PROGRESS"
    FAILURE = "FAILURE"
    SUCCESS = "SUCCESS"


def task_status(task_id: str) -> Status:
    if not is_celery_started():
        logger.warning("celery is not started")
        return Status.FAILURE
    ar = task_result(task_id)
    if ar.successful():
        return Status.SUCCESS
   
    if ar.failed():
        logger.exception(ar.traceback)
        return Status.FAILURE
    
    # ready but not successful => failure
    if ar.ready():  
        return Status.FAILURE
    
    return Status.IN_PROGRESS


def download(task_id: str) -> Optional[Tuple[str, str]]:
    if not is_celery_started():
        logger.warning("celery is not started")
        return None

    ar = task_result(task_id)
    if not ar.successful():
        return None

    upload_filename, to_path = ar.result
    return upload_filename + ".txt", to_path
