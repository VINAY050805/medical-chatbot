import time
from functools import lru_cache

from pinecone import Pinecone
from pinecone import ServerlessSpec

from app.core.config import settings
from app.core.logger import logger
from app.services.embeddings import get_embedding_service


class PineconeService:

    def __init__(self):

        settings.validate_pinecone_settings()

        self.pc = Pinecone(

            api_key=settings.PINECONE_API_KEY

        )

        self.index_name = settings.PINECONE_INDEX_NAME

        self.dimension = get_embedding_service().get_dimension()

        self.index = None

        self.connect()

    # =====================================================
    # Connect
    # =====================================================

    def connect(self):

        try:

            indexes = [

                index["name"]

                for index in self.pc.list_indexes()

            ]

            if self.index_name not in indexes:

                logger.info(

                    "Creating Pinecone Index..."

                )

                self.pc.create_index(

                    name=self.index_name,

                    dimension=self.dimension,

                    metric="cosine",

                    spec=ServerlessSpec(

                        cloud=settings.PINECONE_CLOUD,

                        region=settings.PINECONE_REGION

                    )

                )

                # Wait until index is ready
                deadline = time.time() + 120

                while True:

                    description = self.pc.describe_index(
                        self.index_name
                    )

                    if description.status["ready"]:

                        break

                    logger.info(

                        "Waiting for Pinecone index..."

                    )

                    if time.time() > deadline:

                        raise TimeoutError(
                            "Timed out waiting for Pinecone index to become ready."
                        )

                    time.sleep(2)

            self.index = self.pc.Index(

                self.index_name

            )

            logger.success(

                f"Pinecone Connected "

                f"({self.dimension} dimensions)"

            )

        except Exception as e:

            logger.error(

                f"Pinecone Error: {e}"

            )

            raise

    # =====================================================
    # Health Check
    # =====================================================

    def health_check(self):

        try:

            stats = self.index.describe_index_stats()

            logger.success(

                f"Vectors : "

                f"{stats.total_vector_count}"

            )

            return True

        except Exception as e:

            logger.error(

                f"Pinecone Health Failed: {e}"

            )

            return False

    # =====================================================
    # Stats
    # =====================================================

    def get_stats(self):

        return self.index.describe_index_stats()


@lru_cache(maxsize=1)
def get_pinecone_service():

    return PineconeService()
