from functools import lru_cache

from app.core.prompts import medical_prompt
from app.services.llm import get_llm_service
from app.services.retrieval_service import get_retrieval_service


class RAGService:

    def __init__(self):
        self.llm = get_llm_service().get_llm()
        self.retriever = get_retrieval_service().get_retriever()

    def ask(self, question: str):

        try:

            # Retrieve relevant documents
            documents = self.retriever.invoke(question)

            if not documents:

                return {
                    "answer": "No relevant information was found in the uploaded documents.",
                    "sources": []
                }

            # Build Context
            context = self._build_context(documents)

            # Create Prompt
            prompt = medical_prompt.invoke(
                {
                    "context": context,
                    "input": question
                }
            )

            # LLM Response
            response = self.llm.invoke(prompt)

            return {

                "answer": response.content.strip(),

                "sources": self._extract_sources(documents)

            }

        except Exception as e:

            return {

                "answer": "",

                "sources": [],

                "error": "Unable to generate an answer right now."

            }

    # =====================================================
    # Build Context
    # =====================================================

    def _build_context(self, documents):

        context = []

        for doc in documents:

            source = doc.metadata.get("source", "Unknown")

            page = int(doc.metadata.get("page", 0)) + 1

            context.append(

                f"""
Source : {source}
Page   : {page}

{doc.page_content}
--------------------------------------------------
"""
            )

        return "\n".join(context)

    # =====================================================
    # Extract Sources
    # =====================================================

    def _extract_sources(self, documents):

        seen = set()

        sources = []

        for doc in documents:

            source = doc.metadata.get("source", "Unknown")

            page = int(doc.metadata.get("page", 0)) + 1

            key = (source, page)

            if key not in seen:

                seen.add(key)

                sources.append(
                    {
                        "source": source,
                        "page": page
                    }
                )

        return sources


@lru_cache(maxsize=1)
def get_rag_service():

    return RAGService()
