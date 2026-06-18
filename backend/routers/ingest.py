from fastapi import APIRouter, UploadFile, File
import os
import shutil

from backend.config import settings
from backend.schemas import IngestResponse
from backend.services.rag_service import RagService

router = APIRouter()
_rag = RagService()


@router.post("/ingest", response_model=IngestResponse, summary="Ingest a PDF document")
def ingest(file: UploadFile = File(...)) -> IngestResponse:
    dest_path = os.path.join(settings.DATA_PATH, file.filename)
    with open(dest_path, "wb") as out:
        shutil.copyfileobj(file.file, out)

    response = _rag.ingest_document(dest_path)
    print("RETURNING RESPONSE TO CLIENT")
    return response
"""Accept a PDF upload, save it to the data directory, and trigger ingestion.
    The uploaded file is written to backend/data/ before being passed to
    RagService.ingest_document() for chunking and embedding."""