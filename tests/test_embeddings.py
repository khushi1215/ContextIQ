from backend.rag.ingest import DocumentIngestor
from backend.rag.chunking import TextChunker
from backend.rag.embeddings import EmbeddingGenerator

pdf_path = "backend/data/AWS Customer Agreement.pdf"

ingestor = DocumentIngestor(pdf_path)

text = ingestor.load()

chunker = TextChunker(
    chunk_size=900,
    chunk_overlap=150,
)

chunks = chunker.split(text)

texts = [chunk["text"] for chunk in chunks]

generator = EmbeddingGenerator()

embeddings = generator.embed_batch(texts)

print("\nNumber of chunks:")
print(len(texts))

print("\nEmbedding shape:")
print(embeddings.shape)

print("\nFirst embedding dimension:")
print(len(embeddings[0]))