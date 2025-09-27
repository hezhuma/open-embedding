import os
from .base_loader import BaseLoader
from sentence_transformers import SentenceTransformer
from transformers import pipeline

class HFLoader(BaseLoader):
    def load(self):
        cache_dir = os.path.join(os.path.expanduser("~"), ".cache", "huggingface")
        local_path = self.config.get("local_path")
        model_id = self.model_path

        if local_path and os.path.exists(local_path):
            return SentenceTransformer(local_path)

        try:
            return SentenceTransformer(model_id, cache_folder=cache_dir)
        except Exception:
            # fallback to transformers pipeline
            return pipeline("feature-extraction", model=model_id, cache_dir=cache_dir)
