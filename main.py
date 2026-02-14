import time
from flask import Flask, jsonify

app = Flask(__name__)

@app.get("/")
def home():
    return "AZURE OK", 200

@app.get("/health")
def health():
    return "OK", 200

@app.post("/process")
def process():
    time.sleep(1)   # симулација на работа
    return jsonify({"ok": True})


# важно за локално / Azure compatibility
if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
