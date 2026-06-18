from sentence_transformers import SentenceTransformer
import numpy as np
class EmbeddingGenerator:
    _cached_models = {}

    def __init__(
        self,
        model_name: str = "sentence-transformers/all-MiniLM-L6-v2",
    ) -> None:

        self.model_name = model_name

        if model_name not in EmbeddingGenerator._cached_models:

            print(f"Loading embedding model: {model_name}")

            EmbeddingGenerator._cached_models[model_name] = (
                SentenceTransformer(model_name)
            )

        self.model = EmbeddingGenerator._cached_models[model_name]

    def embed(
        self,
        text: str,
    ) -> np.ndarray:

        return self.model.encode(
            text,
            convert_to_numpy=True,
        )

    def embed_batch(
        self,
        texts: list[str],
    ) -> np.ndarray:

        return self.model.encode(
            texts,
            convert_to_numpy=True,
            show_progress_bar=True,
        )