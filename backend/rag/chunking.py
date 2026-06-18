import re
class TextChunker:
    def __init__(
        self,
        chunk_size: int = 900,
        chunk_overlap: int = 150,
    ) -> None:
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

    def clean(self, text: str) -> str:
        text = text.strip()

        text = re.sub(r"\s+", " ", text)

        return text

    def split(self, text: str) -> list[dict]:
        """
        Returns:
            [
                {
                    "chunk_id": 0,
                    "text": "..."
                }
            ]
        """

        text = self.clean(text)
        chunks = []
        start = 0
        step = self.chunk_size - self.chunk_overlap
        chunk_id = 0
        while start < len(text):
            end = start + self.chunk_size
            chunk_text = text[start:end]
            chunks.append(
                {
                    "chunk_id": chunk_id,
                    "text": chunk_text,
                }
            )
            chunk_id += 1
            start += step
        return chunks