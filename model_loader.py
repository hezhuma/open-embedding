import os
from config import Config
from loaders.hf_loader import HuggingFaceLoader
from loaders.ms_loader import ModelScopeLoader
from loaders.local_loader import LocalLoader

_loaded_models = {}
_model_configs = {}


def init_configs():
    """读取配置文件，但不加载模型"""
    global _model_configs
    cfg = Config()
    # 修复配置解析，models是字典不是列表
    models_dict = cfg.get_models()
    for model_name, model_config in models_dict.items():
        _model_configs[model_name] = model_config
    print(f"已读取配置，共 {len(_model_configs)} 个模型")


def get_loader(model_type, model_name, model_path):
    if model_type == "huggingface":
        return HuggingFaceLoader(model_name, model_path)
    elif model_type == "modelscope":
        return ModelScopeLoader(model_name, model_path)
    elif model_type == "local":
        return LocalLoader(model_name, model_path)
    else:
        raise ValueError(f"未知模型类型: {model_type}")


def get_model(model_name):
    """懒加载 + 缓存"""
    if model_name in _loaded_models:
        print(f"[Cache] 使用缓存模型: {model_name}")
        return _loaded_models[model_name]

    if model_name not in _model_configs:
        raise ValueError(f"模型 {model_name} 未在配置文件中定义")

    cfg = _model_configs[model_name]
    # 对于ModelScope，直接使用配置中的path作为模型ID，不需要添加前缀
    model_path = cfg["path"]
    # 从配置中获取provider
    loader = get_loader(cfg["provider"], model_name, model_path)
    model = loader.load()
    _loaded_models[model_name] = model
    print(f"[OK] 模型 {model_name} 加载完成")
    return model
