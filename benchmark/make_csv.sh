#!/usr/bin/env bash
set -euo pipefail

WORKLOAD="${1:-llm}"
OUT="results/summary_${WORKLOAD}.csv"

echo "rps,gcp_achieved_rps,gcp_avg_ms,gcp_p95_ms,gcp_fail_rate,azure_achieved_rps,azure_avg_ms,azure_p95_ms,azure_fail_rate" > "$OUT"

for f in results/gcp_${WORKLOAD}_*rps.json; do
  r=$(echo "$f" | sed -E 's/.*_([0-9]+)rps\.json/\1/')

  g="results/gcp_${WORKLOAD}_${r}rps.json"
  a="results/azure_${WORKLOAD}_${r}rps.json"

  g_thr=$(jq -r '.metrics.http_reqs.rate // 0' "$g")
  g_avg=$(jq -r '.metrics.http_req_duration.avg // 0' "$g")
  g_p95=$(jq -r '.metrics.http_req_duration["p(95)"] // 0' "$g")
  g_fail=$(jq -r '.metrics.http_req_failed.value // 0' "$g")

  a_thr=$(jq -r '.metrics.http_reqs.rate // 0' "$a")
  a_avg=$(jq -r '.metrics.http_req_duration.avg // 0' "$a")
  a_p95=$(jq -r '.metrics.http_req_duration["p(95)"] // 0' "$a")
  a_fail=$(jq -r '.metrics.http_req_failed.value // 0' "$a")

  echo "${r},${g_thr},${g_avg},${g_p95},${g_fail},${a_thr},${a_avg},${a_p95},${a_fail}" >> "$OUT"
done

{ head -n 1 "$OUT"; tail -n +2 "$OUT" | sort -t, -k1,1n; } > "${OUT}.tmp"
mv "${OUT}.tmp" "$OUT"

echo "Wrote $OUT"
