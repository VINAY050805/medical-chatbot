from pydantic import BaseModel, Field


# =====================================================
# Upload
# =====================================================

class UploadResponse(BaseModel):

    status: str = Field(..., example="success")

    files_uploaded: int = Field(..., example=1)

    message: str = Field(
        ...,
        example="PDF uploaded successfully."
    )


# =====================================================
# Question
# =====================================================

class QuestionRequest(BaseModel):

    question: str = Field(
        ...,
        min_length=1,
        max_length=2000,
        example="What is diabetes?"
    )


class SourceDocument(BaseModel):

    source: str = Field(
        ...,
        example="DIABETES.pdf"
    )

    page: int = Field(
        ...,
        example=3
    )


class QuestionResponse(BaseModel):

    answer: str

    sources: list[SourceDocument]
