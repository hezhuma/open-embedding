import os
from .base_loader import BaseLoader

class ModelScopeLoader(BaseLoader):
    def load(self):
        from modelscope.hub.snapshot_download import snapshot_download
        from sentence_transformers import SentenceTransformer

        cache_dir = os.path.join(os.path.expanduser("~"), ".cache", "modelscope")
        local_path = self.config.get("local_path")
        model_id = self.model_path

        if local_path and os.path.exists(local_path):
            return SentenceTransformer(local_path)

        model_dir = snapshot_download(model_id, cache_dir=cache_dir)
        return SentenceTransformer(model_dir)
