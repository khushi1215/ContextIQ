from pathlib import Path
from pypdf import PdfReader
class DocumentIngestor:
    def __init__(self, file_path: str) -> None:
        self.file_path = file_path
        self.raw_text: str = ""

    def validate(self) -> bool:
        path = Path(self.file_path)

        if not path.exists():
            return False

        if path.suffix.lower() != ".pdf":
            return False

        return True

    def load(self) -> str:
        if not self.validate():
            raise FileNotFoundError(
                f"Invalid PDF file: {self.file_path}"
            )

        reader = PdfReader(self.file_path)

        pages = []

        for page in reader.pages:
            text = page.extract_text()

            if text:
                pages.append(text)

        self.raw_text = "\n".join(pages)

        return self.raw_text