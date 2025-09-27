import os
from .base_loader import BaseLoader
from sentence_transformers import SentenceTransformer

class LocalLoader(BaseLoader):
    def load(self):
        if not os.path.exists(self.model_path):
            raise FileNotFoundError(f"Local model path not found: {self.model_path}")
        return SentenceTransformer(self.model_path)
