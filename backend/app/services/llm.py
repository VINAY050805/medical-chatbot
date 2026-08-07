from langchain_groq import ChatGroq
from functools import lru_cache

from app.core.config import settings
from app.core.logger import logger


class LLMService:

    def __init__(self):

        settings.validate_llm_settings()

        self.model = "llama-3.3-70b-versatile"

        self.llm = ChatGroq(

            api_key=settings.GROQ_API_KEY,

            model=self.model,

            temperature=0.2,

            max_tokens=1024

        )

        logger.success(

            f"Groq LLM Loaded ({self.model})"

        )

    # =====================================================
    # Get LLM
    # =====================================================

    def get_llm(self):

        return self.llm

    # =====================================================
    # Health Check
    # =====================================================

    def health_check(self):

        try:

            self.llm.invoke("Hello")

            logger.success(

                "Groq LLM Healthy"

            )

            return True

        except Exception as e:

            logger.error(

                f"Groq Error : {e}"

            )

            return False


@lru_cache(maxsize=1)
def get_llm_service():

    return LLMService()
