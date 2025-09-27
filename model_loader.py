import importlib
import time
import threading, logging
from config import load_config

logger = logging.getLogger(__name__)
_lock = threading.Lock()
_models = {}
_cfg = None

LOADER_MAP = {
    "local": "loaders.local_loader.LocalLoader",
    "huggingface": "loaders.hf_loader.HFLoader",
    "modelscope": "loaders.ms_loader.ModelScopeLoader"
}

def _resolve_class(spec: str):
    mod_name, cls_name = spec.rsplit(".", 1)
    mod = importlib.import_module(mod_name)
    return getattr(mod, cls_name)

def init_configs(config_path: str = None, preload_all: bool = False):
    """
    初始化模型配置，如果 preload_all=True 则启动时一次性加载所有模型
    """
    global _cfg
    _cfg = load_config(config_path)
    models = _cfg.get("models", [])
    logger.info(f"Loaded {len(models)} model configs")

    for m in models:
        name = m.get("name")
        provider = m.get("provider", "huggingface")
        path = m.get("path")
        if not name or not path:
            logger.warning(f"Skipping invalid model entry: {m}")
            continue

        entry = {"provider": provider, "path": path, "description": m.get("description", ""), **m}

        if preload_all:
            loader_spec = LOADER_MAP.get(provider)
            if not loader_spec:
                logger.error(f"No loader for provider {provider}")
                continue
            LoaderCls = _resolve_class(loader_spec)
            loader = LoaderCls(name, path, config=entry)

            logger.info(f"[{name}] Provider={provider}, path={path}")

            start = time.time()
            try:
                inst = loader.load()
                elapsed = time.time() - start
                logger.info(f"[{name}] ✅ Loaded successfully in {elapsed:.2f}s")
                entry["instance"] = inst
            except Exception as e:
                elapsed = time.time() - start
                logger.error(f"[{name}] ❌ Failed to load in {elapsed:.2f}s. Error: {e}")

        _models[name] = entry

def get_available_models():
    return [{ "name": k, **{kk: vv for kk,vv in v.items() if kk != "instance"} } for k,v in _models.items()]

def get_model(model_name: str):
    if model_name not in _models:
        raise KeyError(f"Model not found: {model_name}")
    entry = _models[model_name]
    if "instance" not in entry:
        raise RuntimeError(f"Model {model_name} not loaded at startup (preload_all required)")
    return entry["instance"]
