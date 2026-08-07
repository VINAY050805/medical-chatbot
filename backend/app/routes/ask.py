from fastapi import APIRouter
from fastapi import HTTPException
from starlette.concurrency import run_in_threadpool

from app.models.schemas import (
    QuestionRequest,
    QuestionResponse,
    SourceDocument
)

from app.services.rag_chain import get_rag_service

router = APIRouter(
    prefix="/ask",
    tags=["Question Answering"]
)


@router.post("/", response_model=QuestionResponse)
async def ask(request: QuestionRequest):

    question = request.question.strip()

    if not question:

        raise HTTPException(
            status_code=422,
            detail="Question cannot be empty."
        )

    result = await run_in_threadpool(
        get_rag_service().ask,
        question
    )

    if result.get("error"):

        raise HTTPException(
            status_code=503,
            detail=result["error"]
        )

    return QuestionResponse(
        answer=result["answer"],
        sources=[
            SourceDocument(**src)
            for src in result["sources"]
        ]
    )
