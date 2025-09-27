from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from model_loader import init_configs, get_model
import torch
import time
import logging

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

logger.info("Starting Embedding Server...")

app = FastAPI(title="Embedding API (OpenAI Compatible)")


class EmbeddingRequest(BaseModel):
    model: str
    input: list[str] | str


@app.on_event("startup")
def startup_event():
    logger.info("Initializing configurations...")
    init_configs()
    logger.info("Configurations initialized successfully.")


@app.post("/v1/embeddings")
def create_embeddings(req: EmbeddingRequest):
    try:
        model_obj = get_model(req.model)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    start = time.time()

    # HuggingFace / ModelScope / Local 统一处理
    if isinstance(model_obj, tuple):  # HuggingFace (model, tokenizer)
        model, tokenizer = model_obj
        texts = [req.input] if isinstance(req.input, str) else req.input
        inputs = tokenizer(texts, return_tensors="pt", padding=True, truncation=True)
        with torch.no_grad():
            embeddings = model(**inputs).last_hidden_state.mean(dim=1).tolist()
    else:
        # ModelScope pipeline 或 Local
        texts = [req.input] if isinstance(req.input, str) else req.input
        if hasattr(model_obj, "__call__"):  # pipeline callable
            embeddings = [model_obj(text)["text_embedding"] for text in texts]
        else:
            embeddings = [model_obj for _ in texts]  # Local placeholder

    duration = round(time.time() - start, 3)
    print(f"[API] 模型 {req.model} 请求完成，用时 {duration}s")

    # 简单 token 统计
    token_count = sum(len(text.split()) for text in texts)

    return {
        "object": "list",
        "data": [
            {
                "object": "embedding",
                "embedding": emb,
                "index": i,
            }
            for i, emb in enumerate(embeddings)
        ],
        "model": req.model,
        "usage": {
            "prompt_tokens": token_count,
            "total_tokens": token_count,
        },
    }


if __name__ == "__main__":
    import uvicorn
    logger.info("Starting Uvicorn server...")
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True, log_level="info")
