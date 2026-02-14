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
    time.sleep(1)
    return jsonify({"ok": True})
