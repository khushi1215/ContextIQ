from backend.rag.ingest import DocumentIngestor

pdf_path = "backend/data/AWS Customer Agreement.pdf"

ingestor = DocumentIngestor(pdf_path)

text = ingestor.load()

print("Characters:", len(text))

print("\nFIRST 1000 CHARACTERS:\n")

print(text[:1000])