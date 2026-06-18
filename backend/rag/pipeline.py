from backend.config import settings
from backend.rag.embeddings import EmbeddingGenerator
from backend.rag.generator import AnswerGenerator
from backend.rag.retrieval import Retriever
from backend.rag.vector_store import VectorStore
class RAGPipeline:
    def __init__(self) -> None:

        print("Initializing RAG pipeline...")

        self.embedder = EmbeddingGenerator(
            settings.EMBEDDING_MODEL
        )

        self.vector_store = VectorStore(
            settings.VECTORSTORE_PATH,
            settings.EMBEDDING_DIMENSION,
        )

        print("Loading FAISS index...")
        self.vector_store.load()
        print("FAISS index loaded.")

        self.retriever = Retriever(
            self.vector_store,
            self.embedder,
        )

        self.generator = AnswerGenerator(
            settings.LLM_MODEL,
        )

        print("RAG pipeline initialized.\n")

    def ask(
        self,
        question: str,
    ) -> dict:

        print("=" * 60)
        print(f"QUESTION: {question}")
        print("=" * 60)

        print("Step 1: Retrieving relevant chunks...")

        chunks = self.retriever.retrieve(
            question,
            settings.TOP_K_RESULTS,
        )

        print(f"Retrieved {len(chunks)} chunks.")

        print("Step 2: Formatting context...")

        context = self.retriever.format_context(
            chunks,
        )

        print(f"Context length: {len(context)} characters.")

        print("Step 3: Sending prompt to Ollama...")

        answer = self.generator.generate(
            question,
            context,
        )

        print("Step 4: Ollama response received.")

        print("=" * 60)
        print("Pipeline completed successfully.")
        print("=" * 60)

        return {
            "answer": answer,
            "sources": chunks,
        }