from pathlib import Path
import os

from dotenv import load_dotenv

# =====================================================
# Load Environment Variables
# =====================================================

BASE_DIR = Path(__file__).resolve().parent.parent.parent

load_dotenv(BASE_DIR / ".env")


class Settings:

    # ==========================
    # Application
    # ==========================

    APP_NAME = os.getenv("APP_NAME", "Medical AI Assistant")

    APP_VERSION = os.getenv("APP_VERSION", "1.0.0")

    DEBUG = os.getenv("DEBUG", "False").lower() == "true"

    CORS_ORIGINS = [
        origin.strip()
        for origin in os.getenv(
            "CORS_ORIGINS",
            "http://localhost:5500,http://127.0.0.1:5500"
        ).split(",")
        if origin.strip()
    ]

    MAX_UPLOAD_FILES = int(os.getenv("MAX_UPLOAD_FILES", "5"))

    MAX_UPLOAD_BYTES = int(os.getenv("MAX_UPLOAD_BYTES", str(10 * 1024 * 1024)))

    # ==========================
    # API Keys
    # ==========================

    # Optional (Used only for Gemini Embeddings)
    # GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

    GROQ_API_KEY = os.getenv("GROQ_API_KEY")

    PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")

    # ==========================
    # Pinecone
    # ==========================

    PINECONE_INDEX_NAME = os.getenv("PINECONE_INDEX_NAME")

    PINECONE_CLOUD = os.getenv("PINECONE_CLOUD")

    PINECONE_REGION = os.getenv("PINECONE_REGION")

    def validate_llm_settings(self):

        missing = [
            name
            for name in ("GROQ_API_KEY",)
            if not getattr(self, name)
        ]

        if missing:

            raise ValueError(
                "Missing required environment variables: "
                + ", ".join(missing)
            )

    def validate_pinecone_settings(self):

        missing = [
            name
            for name in (
                "PINECONE_API_KEY",
                "PINECONE_INDEX_NAME",
                "PINECONE_CLOUD",
                "PINECONE_REGION",
            )
            if not getattr(self, name)
        ]

        if missing:

            raise ValueError(
                "Missing required environment variables: "
                + ", ".join(missing)
            )

    def validate_rag_settings(self):

        self.validate_llm_settings()
        self.validate_pinecone_settings()


settings = Settings()
