# Serverless Containers Benchmark (GCP vs Azure)

## Overview

This project evaluates the performance characteristics of serverless container platforms using:

- **Google Cloud Run (GCP)**
- **Azure Container Apps (Azure)**

The goal is to measure system behavior under increasing load and compare scalability, latency, and throughput.

---

## Workloads

The following workloads were implemented:

1. **CPU-bound task**
   - Endpoint: `/cpu`
   - Behavior: Busy-loop computation
   - Duration: ≥ 5 seconds per request

2. **LLM-style request**
   - Endpoint: `/llm`
   - Payload: 1000-character prompt
   - Purpose: Simulate inference-like processing

3. **File Upload**
   - Endpoint: `/upload`
   - Payload: 1MB raw data

4. **Pub/Sub Message**
   - Endpoint: `/pubsub`
   - Payload: 1KB message

---

## Benchmark Methodology

Load testing was performed using **k6** with a constant arrival rate.

Request rates tested:

- 1
- 10
- 50
- 100
- 200
- 300
- 400
- 500
- 600
- 700
- 800
- 900
- 1000 requests/sec

Each test:

- Duration: 30 seconds
- Metrics captured: latency, throughput, failures

---

## Measured Metrics

The following metrics were analyzed:

- **Execution Time (Latency)**
- **Throughput (Achieved RPS)**
- **Speedup Behavior**

---

## Results

Generated artifacts:

- `execution_time.png`
- `throughput.png`
- `speedup.png`
- `summary_llm.csv`

Key observations:

- Azure shows cold start latency at very low request rates
- GCP exhibits smoother initial response behavior
- Throughput scaling is nearly identical across providers
- Latency degradation occurs under high load

---

## Running the Benchmark

Example k6 execution:

```bash
BASE_URL=<service_url> WORKLOAD=llm RATE=100 k6 run bench.js

Sweep execution:

./sweep.sh gcp <gcp_url> llm
./sweep.sh azure <azure_url> llm

CSV generation:

./make_csv.sh llm


Plot generation:

python3 plot.py

Conclusion

Both Google Cloud Run and Azure Container Apps demonstrate strong horizontal scalability consistent with serverless container platforms.

The benchmark results indicate that throughput scales nearly linearly with increasing request rates, while latency degradation primarily appears under high load conditions.

Azure exhibits noticeable cold start latency at very low request rates, whereas GCP shows smoother initial response behavior. Once instances are active, both platforms deliver comparable performance characteristics.

Overall, the observed differences are attributable to instance lifecycle management and autoscaling dynamics rather than fundamental platform limitations.

Technologies Used

Backend

FastAPI

Python

Cloud Platforms

Google Cloud Run

Azure Container Apps

Benchmarking

k6

Python (matplotlib)

Containerization

Docker
