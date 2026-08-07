from pathlib import Path

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

from app.core.logger import logger


class PDFLoaderService:

    def __init__(self):

        self.splitter = RecursiveCharacterTextSplitter(

            chunk_size=1000,

            chunk_overlap=200,

            separators=[

                "\n\n",

                "\n",

                ".",

                " ",

                ""

            ]

        )

    # =====================================================
    # Load PDF
    # =====================================================

    def load_pdf(self, pdf_path: Path):

        if not pdf_path.exists():

            raise FileNotFoundError(

                f"PDF not found: {pdf_path}"

            )

        try:

            loader = PyPDFLoader(str(pdf_path))

            documents = loader.load()

            logger.info(

                f"Loaded {len(documents)} pages "

                f"from {pdf_path.name}"

            )

            return documents

        except Exception as e:

            logger.error(

                f"Error loading PDF: {e}"

            )

            raise

    # =====================================================
    # Split Documents
    # =====================================================

    def split_documents(self, documents):

        chunks = self.splitter.split_documents(documents)

        logger.info(

            f"Created {len(chunks)} chunks"

        )

        return chunks


pdf_service = PDFLoaderService()