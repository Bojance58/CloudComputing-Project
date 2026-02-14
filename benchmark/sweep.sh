#!/usr/bin/env bash
set -euo pipefail

PROVIDER="${1:-gcp}"
BASE_URL="${2:?BASE_URL missing}"
WORKLOAD="${3:-llm}"

RATES=(1 10 50 100 200 300 400 500 600 700 800 900 1000)

mkdir -p results

for r in "${RATES[@]}"; do
  echo "==> $PROVIDER $WORKLOAD @ ${r} rps"
  BASE_URL="$BASE_URL" WORKLOAD="$WORKLOAD" RATE="$r" CPU_SECONDS="5" \
  PRE_VUS="200" MAX_VUS="500" DURATION="30s" \
  k6 run bench.js --summary-export "results/${PROVIDER}_${WORKLOAD}_${r}rps.json"
done
