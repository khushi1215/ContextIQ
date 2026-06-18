from backend.rag.ingest import DocumentIngestor
from backend.rag.chunking import TextChunker
from backend.rag.embeddings import EmbeddingGenerator
from backend.rag.vector_store import VectorStore

pdf_path = "backend/data/AWS Customer Agreement.pdf"

text = DocumentIngestor(pdf_path).load()

chunks = TextChunker(
    chunk_size=900,
    chunk_overlap=150,
).split(text)

texts = [
    chunk["text"]
    for chunk in chunks
]

embeddings = (
    EmbeddingGenerator()
    .embed_batch(texts)
)

store = VectorStore(
    "backend/vectorstore"
)

store.build(
    embeddings,
    chunks,
)

print(
    "Index built successfully."
)

print(
    f"Vectors stored: {len(chunks)}"
)