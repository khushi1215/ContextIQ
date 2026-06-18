from backend.rag.embeddings import EmbeddingGenerator
from backend.rag.retrieval import Retriever
from backend.rag.vector_store import VectorStore

vector_store = VectorStore(
    "backend/vectorstore"
)

vector_store.load()

embedding_generator = EmbeddingGenerator()

retriever = Retriever(
    vector_store,
    embedding_generator,
)

query = "What happens if AWS changes the agreement?"

results = retriever.retrieve(
    query,
    top_k=3,
)

print("\nTOP RESULTS\n")

for i, result in enumerate(results, start=1):

    print(f"\nResult {i}")
    print(f"Chunk ID: {result['chunk_id']}")

    print(result["text"][:500])

    print("-" * 80)

context = retriever.format_context(
    results
)

print("\nCONTEXT LENGTH:")
print(len(context))