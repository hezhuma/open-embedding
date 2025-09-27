import logging, time
import uvicorn
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from model_loader import init_configs, get_model, get_available_models

logging.basicConfig(level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

app = FastAPI(title="Embedding API (OpenAI Compatible)")

class EmbeddingRequest(BaseModel):
    model: str
    input: object  # str or list[str]

@app.on_event("startup")
def startup_event():
    init_configs(preload_all=True)

@app.get("/v1/models")
def list_models():
    return {"object": "list", "data": get_available_models()}

@app.get("/health")
def health():
    return {"status":"ok","time": int(time.time())}

@app.post("/v1/embeddings")
def create_embeddings(req: EmbeddingRequest):
    texts = req.input
    if isinstance(texts, str):
        texts = [texts]
    if not isinstance(texts, list):
        raise HTTPException(status_code=400, detail="`input` must be a string or list of strings")

    try:
        model = get_model(req.model)
    except KeyError as e:
        raise HTTPException(status_code=404, detail=str(e))

    try:
        if hasattr(model, "encode"):
            embeddings = model.encode(texts, convert_to_numpy=True).tolist()
        elif callable(model):
            embeddings = [model(x).tolist() for x in texts]
        else:
            raise RuntimeError("Unsupported model interface")
    except Exception as e:
        logger.exception("Failed to compute embeddings")
        raise HTTPException(status_code=500, detail=f"Embedding error: {e}")

    data = []
    for i, emb in enumerate(embeddings):
        data.append({"object":"embedding","embedding": emb, "index": i})

    return {
        "object": "list",
        "data": data,
        "model": req.model,
        "usage": {"prompt_tokens": len(texts), "total_tokens": len(texts)}
    }

if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=False)
