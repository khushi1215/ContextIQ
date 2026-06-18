from backend.rag.vector_store import VectorStore
from backend.rag.embeddings import EmbeddingGenerator
class Retriever:
    def __init__(
        self,
        vector_store: VectorStore,
        embedding_generator: EmbeddingGenerator,
    ) -> None:

        self.vector_store = vector_store

        self.embedding_generator = embedding_generator

    def retrieve(
        self,
        query: str,
        top_k: int = 3,
    ) -> list[dict]:
        """
        Retrieve top-k relevant chunks.
        """

        query_embedding = (
            self.embedding_generator.embed(query)
        )

        results = self.vector_store.search(
            query_embedding,
            top_k=top_k,
        )

        return results

    def format_context(
        self,
        chunks: list[dict],
    ) -> str:
        """
        Convert retrieved chunks into
        a single context string.
        """

        context = "\n\n".join(
            chunk["text"]
            for chunk in chunks
        )

        return context