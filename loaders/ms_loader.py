from .base_loader import BaseLoader
from modelscope.pipelines import pipeline
from modelscope.utils.constant import Tasks
import os


class ModelScopeLoader(BaseLoader):
    def load(self):
        print(f"[MS] 懒加载 ModelScope 模型: {self.model_name} ({self.model_path})")
        # 获取设备配置（默认为CPU）
        device = os.getenv("DEVICE", "cpu")
        device_id = 0 if device in ["cuda", "npu"] else -1
        # 使用正确的sentence_embedding任务类型
        model = pipeline(Tasks.sentence_embedding, model=self.model_path, device=device_id)
        return model
