from backend.rag.pipeline import RAGPipeline

pipeline = RAGPipeline()

question = "What happens if AWS changes the agreement?"

result = pipeline.ask(question)

print("\nANSWER\n")

print(result["answer"])

print("\nSOURCES\n")

for source in result["sources"]:

    print(f"Chunk {source['chunk_id']}")