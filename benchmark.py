import time
import asyncio
import aiohttp
import statistics
import matplotlib.pyplot as plt

VLLM_URL = "http://localhost:8000/v1/chat/completions"
FRIENDLI_URL = "http://localhost:9000/v1/chat/completions"

MODEL_NAME = "fake-model"
PROMPT = "Explain what cloud computing is in simple terms."
MAX_TOKENS = 128

CONCURRENCY_LEVELS = [1, 2, 4, 8, 16]
REQUESTS_PER_LEVEL = 20


async def send_request(session, url):
    payload = {
        "model": MODEL_NAME,
        "messages": [{"role": "user", "content": PROMPT}],
        "max_tokens": MAX_TOKENS,
        "temperature": 0.0
    }

    start = time.perf_counter()
    async with session.post(url, json=payload) as resp:
        data = await resp.json()
    end = time.perf_counter()

    tokens = data["usage"]["completion_tokens"]
    latency = end - start
    tps = tokens / latency

    return latency, tps


async def run_benchmark(url, concurrency):
    latencies = []
    throughputs = []

    connector = aiohttp.TCPConnector(limit=concurrency)
    async with aiohttp.ClientSession(connector=connector) as session:
        tasks = [send_request(session, url) for _ in range(REQUESTS_PER_LEVEL)]
        results = await asyncio.gather(*tasks)

    for latency, tps in results:
        latencies.append(latency)
        throughputs.append(tps)

    return statistics.mean(throughputs)


async def main():
    vllm_results = []
    friendli_results = []

    for c in CONCURRENCY_LEVELS:
        print(f"Running concurrency {c}")
        vllm_results.append(await run_benchmark(VLLM_URL, c))
        friendli_results.append(await run_benchmark(FRIENDLI_URL, c))

    plt.plot(CONCURRENCY_LEVELS, vllm_results, label="vLLM")
    plt.plot(CONCURRENCY_LEVELS, friendli_results, label="Friendli Engine")
    plt.xlabel("Concurrency")
    plt.ylabel("Tokens per Second")
    plt.title("Inference Throughput Comparison")
    plt.legend()
    plt.savefig("throughput.png")
    plt.show()


if __name__ == "__main__":
    asyncio.run(main())
