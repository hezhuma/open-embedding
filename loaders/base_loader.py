class BaseLoader:
    def __init__(self, name: str, model_path: str, config: dict = None):
        self.name = name
        self.model_path = model_path
        self.config = config or {}

    def load(self):
        raise NotImplementedError
