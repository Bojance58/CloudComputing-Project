import os
import time
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.get("/health")
def health():
    return "OK", 200

@app.post("/process")
def process():
    # Accept payload (e.g. 1000 chars) but do not spend CPU on it
    _ = request.get_json(silent=True) or {}

    # "Workload >= 5s" (LLM-like / I/O-like): sleep, not CPU busy loop
    # You can set WORK_SECONDS=5 in Azure App settings if you want.
    work_s = float(os.getenv("WORK_SECONDS", "5.0"))

    start = time.perf_counter()
    time.sleep(work_s)   # IMPORTANT: keeps CPU low, still >=5s end-to-end time
    elapsed = time.perf_counter() - start

    return jsonify({"elapsed_s": elapsed, "work_s": work_s}), 200
