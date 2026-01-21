# Inference Engine Benchmark (Q3)

## Overview

This project benchmarks inference efficiency between:
- an open-source inference engine (e.g., vLLM)
- the Friendli Engine

The benchmark measures throughput (tokens per second) under increasing concurrency and generates a single graph that visualizes the performance gap.

The design follows the assignment instruction:
“You may assume both vLLM and Friendli Engine are already deployed.”

To make the benchmark easy to test and reproducible, this repository supports two modes:
1. Real mode – benchmark real deployed engines
2. Demo mode – benchmark locally simulated engines (no real models required)

---

## Metrics Used

### Tokens per Second (Throughput)

Throughput was selected because it:
- Directly measures decoding efficiency
- Reflects batching and scheduler performance
- Scales meaningfully with concurrency
- Is easy to interpret for both technical and non-technical stakeholders

The benchmark plots:
- Throughput vs Concurrency

This single visualization clearly demonstrates inference efficiency differences.

---

## Files in This Repository

.
├── benchmark.py  
├── fake_engine.py  
├── requirements.txt  
├── README.md  

---

## Installation

Install Python dependencies:

pip install -r requirements.txt

Python version required: 3.11 or higher

---

## MODE 1 — Benchmark REAL Engines (Production Scenario)

Use this mode if:
- vLLM is already deployed
- Friendli Engine is already deployed

### Required Endpoints

vLLM API:
http://localhost:8000/v1/chat/completions

Friendli Engine API:
http://localhost:9000/v1/chat/completions

If your endpoints use different hosts or ports, update these lines in benchmark.py:

VLLM_URL = "http://<HOST>:<PORT>/v1/chat/completions"  
FRIENDLI_URL = "http://<HOST>:<PORT>/v1/chat/completions"

And update MODEL_NAME also

### Run the Benchmark

python benchmark.py

### Output

A graph named throughput.png is generated.
The graph compares throughput vs concurrency for both engines.

---

## MODE 2 — Demo Mode (No Real Engines Required)

This mode is provided to:
- Test the benchmark logic
- Generate sample results
- Allow reviewers to run the project easily

Two lightweight local servers simulate:
- vLLM (slower)
- Friendli Engine (faster)

---

### Step 1 — Start Fake vLLM (Port 8000)

python fake_engine.py --port 8000 --engine-name vLLM --model fake-model --prefill-ms 80 --per-token-ms 4 --tokens 128

---

### Step 2 — Start Fake Friendli Engine (Port 9000)

Open a second terminal and run:

python fake_engine.py --port 9000 --engine-name Friendli --model fake-model --prefill-ms 30 --per-token-ms 2 --tokens 128

---

### Step 3 — Run the Benchmark

Open a third terminal and run:

python benchmark.py

---

## Stopping the Servers

Press Ctrl + C in each server terminal.

---

## Interpretation of Results

- Higher throughput means more efficient inference
- Better scaling at higher concurrency indicates superior scheduling and batching
- The graph makes efficiency differences easy to understand


