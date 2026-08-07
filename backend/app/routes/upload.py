from fastapi import APIRouter
from fastapi import UploadFile
from fastapi import File
from fastapi import HTTPException
from starlette.concurrency import run_in_threadpool
from app.core.logger import logger
from app.core.config import settings

from app.models.schemas import UploadResponse

from app.services.document_processor import document_processor

router = APIRouter(

    prefix="/upload",

    tags=["Upload"]

)


@router.post("/", response_model=UploadResponse)
async def upload_pdfs(files: list[UploadFile] = File(...)):

    if len(files) > settings.MAX_UPLOAD_FILES:

        raise HTTPException(
            status_code=413,
            detail=f"Upload a maximum of {settings.MAX_UPLOAD_FILES} PDFs at once."
        )

    uploaded = 0

    for file in files:

        if not file.filename or not file.filename.lower().endswith(".pdf"):
            raise HTTPException(
                status_code=400,
                detail="Only PDF files are allowed."
            )

        if file.content_type not in (None, "", "application/pdf"):

            raise HTTPException(
                status_code=400,
                detail="Only PDF files are allowed."
            )

        try:
            pdf_path = await run_in_threadpool(
                document_processor.save_pdf,
                file
            )

            result = await run_in_threadpool(
                document_processor.process_pdf,
                pdf_path
            )

            logger.info(f"File: {file.filename}")
            logger.info(f"Pages: {result['pages']}")
            logger.info(f"Chunks: {result['chunks']}")
            logger.info(f"Indexed: {result['indexed']}")

            uploaded += 1

        except HTTPException:

            raise

        except Exception as e:
            logger.error(f"Upload failed: {e}")
            raise HTTPException(
                status_code=500,
                detail="Unable to process uploaded PDF."
            )

    return UploadResponse(
        status="success",
        files_uploaded=uploaded,
        message="PDF uploaded successfully."
    )
