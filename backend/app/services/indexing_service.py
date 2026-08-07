from pathlib import Path
from functools import lru_cache

from app.core.logger import logger
from app.services.embeddings import get_embedding_service
from app.services.pinecone_store import get_pinecone_service


class IndexingService:

    def __init__(self):

        self.embedding = get_embedding_service().get_embeddings()

        self.index = get_pinecone_service().index

    def index_documents(self, documents, filename):

        if not documents:

            logger.warning("No documents found to index.")

            return 0

        texts = [doc.page_content for doc in documents]
        embeddings = self.embedding.embed_documents(texts)

        vectors = []

        for chunk_number, doc in enumerate(documents):

            try:

                vector_id = (
                    f"{Path(filename).stem}"
                    f"_page{doc.metadata.get('page', 0)}"
                    f"_chunk{chunk_number}"
                )

                vectors.append(
                    {
                        "id": vector_id,

                        "values": embeddings[chunk_number],

                        "metadata": {

                            "text": doc.page_content,

                            "source": Path(filename).name,

                            "page": int(doc.metadata.get("page", 0)),

                            "chunk": chunk_number

                        }

                    }
                )

            except Exception as e:

                logger.error(

                    f"Embedding failed for chunk "

                    f"{chunk_number}: {e}"

                )

        if not vectors:

            logger.warning(

                "No vectors generated."

            )

            return 0

        batch_size = 100

        for start in range(0, len(vectors), batch_size):

            self.index.upsert(vectors=vectors[start:start + batch_size])

        logger.success(

            f"Indexed {len(vectors)} chunks "

            f"from {filename}"

        )

        return len(vectors)


@lru_cache(maxsize=1)
def get_indexing_service():

    return IndexingService()
