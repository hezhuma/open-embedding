import os, yaml

def load_config(path=None):
    if not path:
        path = os.environ.get("MODEL_CONFIG", "config/models.yaml")
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)
