import asyncio, time, csv, statistics, ssl
import aiohttp
#URL = "https://workapp-170765046354.europe-west1.run.app/process" # gcp
URL = "https://pvoprojekt2026.azurewebsites.net/process" #azure

RPS_LEVELS = [1, 10, 50, 100, 200, 300, 400, 500, 600, 700, 800, 900, 1000]
DURATION_SECONDS = 20
WARMUP_SECONDS = 5
CONCURRENCY_CAP = 2000

PAYLOAD = {"prompt": "Generate answer: " + ("x" * 980)}  # ~1000 chars

async def worker(session, queue, latencies, statuses):
    while True:
        token = await queue.get()
        if token is None:
            queue.task_done()
            return

        start = time.perf_counter()
        ok = 0
        try:
            async with session.post(URL, json=PAYLOAD, timeout=aiohttp.ClientTimeout(total=60)) as resp:
                await resp.read()
                ok = 1 if resp.status == 200 else 0
        except Exception:
            ok = 0

        latencies.append(time.perf_counter() - start)
        statuses.append(ok)
        queue.task_done()

async def run_level(rps: int):
    total_seconds = WARMUP_SECONDS + DURATION_SECONDS
    concurrency = min(max(1, int(rps * 6)), CONCURRENCY_CAP)  # service ~5s

    queue = asyncio.Queue(maxsize=concurrency * 5)
    latencies, statuses = [], []

    ssl_ctx = ssl.create_default_context()
    connector = aiohttp.TCPConnector(limit=0, ssl=ssl_ctx, ttl_dns_cache=300)

    async with aiohttp.ClientSession(connector=connector) as session:
        workers = [asyncio.create_task(worker(session, queue, latencies, statuses))
                   for _ in range(concurrency)]

        start_time = time.perf_counter()
        next_send = start_time
        sent = 0

        while True:
            now = time.perf_counter()
            if now - start_time >= total_seconds:
                break

            if now >= next_send:
                await queue.put(1)
                sent += 1
                next_send += 1.0 / rps
            else:
                await asyncio.sleep(min(0.001, next_send - now))

        await queue.join()
        for _ in workers:
            await queue.put(None)
        await asyncio.gather(*workers)

    warmup_cut = rps * WARMUP_SECONDS
    lat = latencies[warmup_cut:] if len(latencies) > warmup_cut else latencies
    st  = statuses[warmup_cut:] if len(statuses) > warmup_cut else statuses

    success = sum(st)
    total = len(st)
    throughput = success / DURATION_SECONDS if DURATION_SECONDS else 0.0

    if lat:
        avg = statistics.mean(lat)
        p95 = statistics.quantiles(lat, n=20)[18] if len(lat) >= 20 else sorted(lat)[max(0, int(0.95*len(lat))-1)]
        mn, mx = min(lat), max(lat)
    else:
        avg = p95 = mn = mx = 0.0

    return {
        "rps_target": rps,
        "requests_sent": sent,
        "requests_measured": total,
        "success": success,
        "success_rate": (success / total) if total else 0.0,
        "throughput_rps": throughput,
        "avg_latency_s": avg,
        "p95_latency_s": p95,
        "min_latency_s": mn,
        "max_latency_s": mx,
    }

async def main():
    results = []
    for rps in RPS_LEVELS:
        print(f"\n=== Testing {rps} req/s ===")
        res = await run_level(rps)
        results.append(res)
        print(res)

    with open("results.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(results[0].keys()))
        w.writeheader()
        w.writerows(results)

    print("\nSaved results.csv")

if __name__ == "__main__":
    asyncio.run(main())
