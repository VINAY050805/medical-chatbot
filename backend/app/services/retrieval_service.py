from langchain_pinecone import PineconeVectorStore
from functools import lru_cache

from app.services.embeddings import get_embedding_service
from app.services.pinecone_store import get_pinecone_service


class RetrievalService:

    def __init__(self):

        self.vector_store = PineconeVectorStore(

            index=get_pinecone_service().index,

            embedding=get_embedding_service().get_embeddings(),

            text_key="text"

        )

    def get_retriever(

        self,

        k: int = 5,

        fetch_k: int = 20

    ):

        """
        Returns a retriever configured for RAG.

        search_type:
            similarity
            similarity_score_threshold
            mmr

        Default:
            MMR (Maximum Marginal Relevance)
        """

        return self.vector_store.as_retriever(

            search_type="mmr",

            search_kwargs={

                "k": k,

                "fetch_k": fetch_k,

                "lambda_mult": 0.7

            }

        )


@lru_cache(maxsize=1)
def get_retrieval_service():

    return RetrievalService()
