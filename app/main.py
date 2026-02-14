from fastapi import FastAPI, Request
import time

app = FastAPI()

@app.get("/")
def root():
    return {"ok": True}

@app.post("/cpu")
async def cpu(payload: dict):
    seconds = int(payload.get("seconds", 5))
    end = time.time() + seconds
    x = 0
    while time.time() < end:
        x = (x * 3 + 7) % 1000003
    return {"done": True, "seconds": seconds}

@app.post("/llm")
async def llm(payload: dict):
    prompt = payload.get("prompt", "")
    return {"len": len(prompt)}

@app.post("/upload")
async def upload(req: Request):
    data = await req.body()
    return {"bytes": len(data)}

@app.post("/pubsub")
async def pubsub(payload: dict):
    msg = payload.get("msg", "")
    return {"bytes": len(msg)}
