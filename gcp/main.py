import os
import time
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.post("/process")
def process():
    data = request.get_json(silent=True) or {}
    start = time.time()
    while time.time() - start < 5:
        pass
    return jsonify({
        "ok": True,
        "prompt_len": len(data.get("prompt", "")),
        "duration": time.time() - start
    })

@app.get("/health")
def health():
    return "OK", 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", "8080"))
    app.run(host="0.0.0.0", port=port)
