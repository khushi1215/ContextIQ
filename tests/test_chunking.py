from backend.rag.ingest import DocumentIngestor
from backend.rag.chunking import TextChunker

pdf_path = "backend/data/AWS Customer Agreement.pdf"

ingestor = DocumentIngestor(pdf_path)

text = ingestor.load()

chunker = TextChunker(
    chunk_size=900,
    chunk_overlap=150,
)

chunks = chunker.split(text)

print(f"\nTotal Chunks: {len(chunks)}")

print("\nFIRST CHUNK\n")
print(chunks[0]["text"][:300])

print("\nSECOND CHUNK\n")
print(chunks[1]["text"][:300])

print("\nLAST CHUNK\n")
print(chunks[-1]["text"][:300])