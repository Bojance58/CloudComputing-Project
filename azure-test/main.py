import os
import time
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/")
def home():
    return "AZURE WORKS", 200

@app.route("/health")
def health():
    return "OK", 200

@app.route("/process", methods=["POST"])
def process():
    data = request.get_json(silent=True) or {}
    time.sleep(1)  # кратка симулација
    return jsonify({
        "ok": True,
        "len": len(data.get("prompt", ""))
    })
