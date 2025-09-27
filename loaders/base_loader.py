class BaseLoader:
    """基础模型加载器"""
    def __init__(self, model_name, model_path):
        self.model_name = model_name
        self.model_path = model_path

    def load(self):
        raise NotImplementedError("子类需要实现 load() 方法")
