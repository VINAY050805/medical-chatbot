from pathlib import Path

from fastapi import HTTPException, UploadFile

from app.core.logger import logger
from app.services.pdf_loader import pdf_service
from app.services.indexing_service import get_indexing_service
from app.core.config import settings


class DocumentProcessor:

    def __init__(self):

        self.upload_dir = Path("uploaded_docs")
        self.upload_dir.mkdir(parents=True, exist_ok=True)

    # =====================================================
    # Save Uploaded PDF
    # =====================================================

    def save_pdf(self, file: UploadFile) -> Path:

        filename = Path(file.filename or "").name

        if not filename.lower().endswith(".pdf"):

            raise HTTPException(

                status_code=400,

                detail="Only PDF files are allowed."

            )

        if filename != file.filename or any(char in filename for char in ("\\", "/")):

            raise HTTPException(

                status_code=400,

                detail="Invalid filename."

            )

        try:

            file.file.seek(0)

            if file.file.read(5) != b"%PDF-":

                raise HTTPException(

                    status_code=400,

                    detail="Invalid PDF file."

                )

            file.file.seek(0)

        except HTTPException:

            raise

        except Exception:

            raise HTTPException(

                status_code=400,

                detail="Unable to read uploaded file."

            )

        destination = self.upload_dir / filename

        try:

            if destination.exists():

                stem = destination.stem
                suffix = destination.suffix
                counter = 1

                while destination.exists():

                    destination = self.upload_dir / f"{stem}_{counter}{suffix}"

                    counter += 1

            with destination.open("wb") as buffer:

                total = 0

                while chunk := file.file.read(1024 * 1024):

                    total += len(chunk)

                    if total > settings.MAX_UPLOAD_BYTES:

                        destination.unlink(missing_ok=True)

                        raise HTTPException(

                            status_code=413,

                            detail="PDF is too large."

                        )

                    buffer.write(chunk)

            logger.success(

                f"Saved PDF : {destination.name}"

            )

            return destination

        except Exception as e:

            logger.error(

                f"Failed to save PDF : {e}"

            )

            if isinstance(e, HTTPException):

                raise e

            raise HTTPException(

                status_code=500,

                detail=f"Unable to save PDF: {str(e)}"

            )

    # =====================================================
    # Process PDF
    # =====================================================

    def process_pdf(self, pdf_path: Path):

        try:

            documents = pdf_service.load_pdf(pdf_path)

            chunks = pdf_service.split_documents(documents)

            indexed = get_indexing_service().index_documents(

                chunks,

                pdf_path.name

            )

            logger.info(

                f"""
============================================================
File     : {pdf_path.name}
Pages    : {len(documents)}
Chunks   : {len(chunks)}
Indexed  : {indexed}
============================================================
"""
            )

            return {

                "pages": len(documents),

                "chunks": len(chunks),

                "indexed": indexed

            }

        except Exception as e:

            logger.error(

                f"Processing failed : {e}"

            )

            raise HTTPException(

                status_code=500,

                detail=str(e)

            )


document_processor = DocumentProcessor()
