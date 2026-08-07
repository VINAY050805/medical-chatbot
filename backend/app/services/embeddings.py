from langchain_huggingface import HuggingFaceEmbeddings

from app.core.logger import logger
from functools import lru_cache


class EmbeddingService:

    def __init__(self):

        self.model = "BAAI/bge-base-en-v1.5"

        self.embeddings = HuggingFaceEmbeddings(

            model_name=self.model,

            model_kwargs={

                "device": "cpu"

            },

            encode_kwargs={

                "normalize_embeddings": True

            }

        )

        self.dimension = 768

        logger.success(

            f"Embedding Model Loaded : {self.model}"

        )

    def get_embeddings(self):

        return self.embeddings

    def get_dimension(self):

        return self.dimension


@lru_cache(maxsize=1)
def get_embedding_service():

    return EmbeddingService()


# =====================================================
# Gemini Embeddings
# =====================================================

# from langchain_google_genai import GoogleGenerativeAIEmbeddings

# self.embeddings = GoogleGenerativeAIEmbeddings(
#     model="gemini-embedding-001",
#     google_api_key=settings.GOOGLE_API_KEY
# )
#
# self.dimension = 3072
