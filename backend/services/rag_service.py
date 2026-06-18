import os
import time

from backend.config import settings
from backend.rag.chunking import TextChunker
from backend.rag.embeddings import EmbeddingGenerator
from backend.rag.ingest import DocumentIngestor
from backend.rag.pipeline import RAGPipeline
from backend.rag.vector_store import VectorStore
from backend.schemas import AskResponse, IngestResponse


class RagService:

    def ingest_document(
        self,
        file_path: str,
    ) -> IngestResponse:

        try:

            print("STEP 1: Loading PDF")

            ingestor = DocumentIngestor(file_path)

            text = ingestor.load()

            print("STEP 2: Chunking")

            chunker = TextChunker(
                settings.CHUNK_SIZE,
                settings.CHUNK_OVERLAP,
            )

            chunks = chunker.split(text)

            print(f"Chunks: {len(chunks)}")

            texts = [
                chunk["text"]
                for chunk in chunks
            ]

            print("STEP 3: Creating embeddings")

            embeddings = (
                EmbeddingGenerator(
                    settings.EMBEDDING_MODEL
                ).embed_batch(texts)
            )

            print(f"Embeddings: {len(embeddings)}")

            filename = os.path.basename(file_path)

            metadata = []

            for chunk in chunks:
                metadata.append(
                    {
                        "chunk_id": chunk["chunk_id"],
                        "source": filename,
                        "text": chunk["text"],
                    }
                )

            print("STEP 4: Building FAISS")

            store = VectorStore(
                settings.VECTORSTORE_PATH,
                settings.EMBEDDING_DIMENSION,
            )

            store.build(
                embeddings,
                metadata,
            )

            print("STEP 5: Done")

            return IngestResponse(
                message=f"{filename} ingested successfully."
            )

        except Exception:
            print("\n\nERROR OCCURRED\n")
            raise

    def ask_question(
        self,
        query: str,
    ) -> AskResponse:

        start = time.time()

        pipeline = RAGPipeline()

        result = pipeline.ask(query)

        latency = (time.time() - start) * 1000

        return AskResponse(
            answer=result["answer"],
            sources=[
                f'{chunk["source"]} (Chunk {chunk["chunk_id"]})'
                for chunk in result["sources"]
            ],
            latency_ms=round(latency, 2),
        )