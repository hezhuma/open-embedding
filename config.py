import yaml
import os


class Config:
    def __init__(self, config_file="config/models.yaml"):
        if not os.path.exists(config_file):
            raise FileNotFoundError(f"配置文件不存在: {config_file}")
        with open(config_file, "r", encoding="utf-8") as f:
            self.config = yaml.safe_load(f)

    def get_models(self):
        return self.config.get("models", [])
