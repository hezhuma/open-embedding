from .base_loader import BaseLoader
import os
from modelscope.pipelines import pipeline
from modelscope.utils.constant import Tasks


class LocalLoader(BaseLoader):
    def load(self):
        print(f"[Local] 懒加载本地模型: {self.model_name} ({self.model_path})")
        if not os.path.exists(self.model_path):
            raise FileNotFoundError(f"路径不存在: {self.model_path}\n请确保模型已下载到本地，可使用modelscope下载命令：\nmodelscope download --model {self.model_path}")
        
        # 获取设备配置（默认为CPU）
        device = os.getenv("DEVICE", "cpu")
        device_id = 0 if device in ["cuda", "npu"] else -1
        
        # 使用local_files_only=True确保从本地加载
        model = pipeline(
            Tasks.sentence_embedding, 
            model=self.model_path, 
            device=device_id,
            model_revision=None,  # 不指定版本
            local_files_only=True  # 仅使用本地文件
        )
        return model
