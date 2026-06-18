import json
from pathlib import Path
import faiss
import numpy as np
class VectorStore:
    def __init__(
        self,
        index_path: str,
        dimension: int = 384,
    ) -> None:

        self.index_path = Path(index_path)

        self.dimension = dimension

        self.index = None

        self.metadata: list[dict] = []

        self.index_file = self.index_path / "faiss_index.bin"

        self.metadata_file = self.index_path / "chunks.json"

    def build(
        self,
        embeddings,
        metadata: list[dict],
    ) -> None:

        embeddings = np.array(
            embeddings,
            dtype=np.float32,
        )

        self.index = faiss.IndexFlatL2(
            self.dimension
        )

        self.index.add(embeddings)

        self.metadata = metadata

        self.save()

    def search(
        self,
        query_embedding,
        top_k: int = 3,
    ) -> list[dict]:

        if self.index is None:
            raise ValueError(
                "FAISS index not loaded."
            )

        query_embedding = np.array(
            [query_embedding],
            dtype=np.float32,
        )

        distances, indices = self.index.search(
            query_embedding,
            top_k,
        )

        results = []

        for idx in indices[0]:

            if idx < len(self.metadata):

                results.append(
                    self.metadata[idx]
                )

        return results

    def save(self) -> None:

        self.index_path.mkdir(
            parents=True,
            exist_ok=True,
        )

        faiss.write_index(
            self.index,
            str(self.index_file),
        )

        with open(
            self.metadata_file,
            "w",
            encoding="utf-8",
        ) as f:

            json.dump(
                self.metadata,
                f,
                ensure_ascii=False,
                indent=2,
            )

    def load(self) -> None:

        self.index = faiss.read_index(
            str(self.index_file)
        )

        with open(
            self.metadata_file,
            "r",
            encoding="utf-8",
        ) as f:

            self.metadata = json.load(f)