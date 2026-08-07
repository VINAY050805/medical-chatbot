from pathlib import Path

from app.services.pdf_loader import pdf_service

pdf = Path("uploaded_docs/BEST_RESUME.pdf")

documents = pdf_service.load_pdf(pdf)

chunks = pdf_service.split_documents(documents)

print(len(documents))

print(len(chunks))

print(chunks[0].page_content)