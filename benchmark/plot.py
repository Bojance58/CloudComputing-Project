import csv
import matplotlib.pyplot as plt

csv_path = "results/summary_llm.csv"

rps = []
g_avg = []; g_p95 = []; g_thr = []; g_speed = []
a_avg = []; a_p95 = []; a_thr = []; a_speed = []

with open(csv_path, newline="") as f:
    rows = list(csv.DictReader(f))

g_base = float(rows[0]["gcp_avg_ms"])
a_base = float(rows[0]["azure_avg_ms"])

for row in rows:
    r = float(row["rps"])
    rps.append(r)

    gthr = float(row["gcp_achieved_rps"])
    gavg = float(row["gcp_avg_ms"])
    gp95 = float(row["gcp_p95_ms"])

    athr = float(row["azure_achieved_rps"])
    aavg = float(row["azure_avg_ms"])
    ap95 = float(row["azure_p95_ms"])

    g_thr.append(gthr); g_avg.append(gavg); g_p95.append(gp95)
    a_thr.append(athr); a_avg.append(aavg); a_p95.append(ap95)

    g_speed.append(g_base / gavg if gavg else 0)
    a_speed.append(a_base / aavg if aavg else 0)

# Execution Time (p95)
plt.figure()
plt.plot(rps, g_p95, label="GCP p95")
plt.plot(rps, a_p95, label="Azure p95")
plt.xscale("log")
plt.xlabel("Target RPS")
plt.ylabel("Latency p95 (ms)")
plt.title("Execution Time vs Load (LLM)")
plt.legend()
plt.grid()
plt.savefig("results/execution_time.png", dpi=150)

# Throughput
plt.figure()
plt.plot(rps, g_thr, label="GCP achieved")
plt.plot(rps, a_thr, label="Azure achieved")
plt.xscale("log")
plt.xlabel("Target RPS")
plt.ylabel("Achieved RPS")
plt.title("Throughput vs Load (LLM)")
plt.legend()
plt.grid()
plt.savefig("results/throughput.png", dpi=150)

# Speedup / Slowdown indicator
plt.figure()
plt.plot(rps, g_speed, label="GCP speedup")
plt.plot(rps, a_speed, label="Azure speedup")
plt.xscale("log")
plt.xlabel("Target RPS")
plt.ylabel("Baseline / Latency")
plt.title("Speedup vs Load (LLM)")
plt.legend()
plt.grid()
plt.savefig("results/speedup.png", dpi=150)

print("Plots saved in results/")
