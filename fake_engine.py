import argparse
import asyncio
import time
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import uvicorn

app = FastAPI()

# These will be set from CLI args
ENGINE_NAME = "fake"
MODEL_NAME = "fake-model"
PREFILL_DELAY_MS = 50       # affects "time to start responding"
PER_TOKEN_DELAY_MS = 3      # affects tokens/sec (decode speed)
TOKENS_PER_RESPONSE = 128   # how many completion tokens we claim to generate


@app.get("/v1/models")
async def models():
    return {
        "object": "list",
        "data": [{"id": MODEL_NAME, "object": "model"}]
    }


@app.post("/v1/chat/completions")
async def chat_completions(request: Request):
    _ = await request.json()

    # Simulate work:
    # 1) prefill delay
    await asyncio.sleep(PREFILL_DELAY_MS / 1000.0)

    # 2) decode delay proportional to tokens
    await asyncio.sleep((PER_TOKEN_DELAY_MS * TOKENS_PER_RESPONSE) / 1000.0)

    # Return OpenAI-ish response shape
    content = f"[{ENGINE_NAME}] This is a simulated response."
    return JSONResponse({
        "id": f"chatcmpl-{int(time.time()*1000)}",
        "object": "chat.completion",
        "created": int(time.time()),
        "model": MODEL_NAME,
        "choices": [{
            "index": 0,
            "message": {"role": "assistant", "content": content},
            "finish_reason": "stop"
        }],
        "usage": {
            "prompt_tokens": 20,
            "completion_tokens": TOKENS_PER_RESPONSE,
            "total_tokens": 20 + TOKENS_PER_RESPONSE
        }
    })


def main():
    global ENGINE_NAME, MODEL_NAME, PREFILL_DELAY_MS, PER_TOKEN_DELAY_MS, TOKENS_PER_RESPONSE

    parser = argparse.ArgumentParser()
    parser.add_argument("--port", type=int, required=True)
    parser.add_argument("--engine-name", type=str, default="fake")
    parser.add_argument("--model", type=str, default="fake-model")
    parser.add_argument("--prefill-ms", type=int, default=50)
    parser.add_argument("--per-token-ms", type=int, default=3)
    parser.add_argument("--tokens", type=int, default=128)
    args = parser.parse_args()

    ENGINE_NAME = args.engine_name
    MODEL_NAME = args.model
    PREFILL_DELAY_MS = args.prefill_ms
    PER_TOKEN_DELAY_MS = args.per_token_ms
    TOKENS_PER_RESPONSE = args.tokens

    uvicorn.run(app, host="0.0.0.0", port=args.port, log_level="warning")


if __name__ == "__main__":
    main()
