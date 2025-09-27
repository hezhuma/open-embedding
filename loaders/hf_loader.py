from .base_loader import BaseLoader
from transformers import AutoModel, AutoTokenizer


class HuggingFaceLoader(BaseLoader):
    def load(self):
        print(f"[HF] 懒加载 HuggingFace 模型: {self.model_name} ({self.model_path})")
        tokenizer = AutoTokenizer.from_pretrained(self.model_path, local_files_only=True)
        model = AutoModel.from_pretrained(self.model_path, local_files_only=True)
        return model, tokenizer
