from __future__ import annotations

import argparse
import os

import httpx


def main() -> None:
    parser = argparse.ArgumentParser(description="Test the local AI Gateway")
    parser.add_argument("--url", default=os.getenv("GATEWAY_URL", "http://127.0.0.1:8000"))
    parser.add_argument("--message", default="Say hello in one short sentence.")
    args = parser.parse_args()

    headers = {}
    gateway_key = os.getenv("GATEWAY_API_KEY")
    if gateway_key:
        headers["Authorization"] = f"Bearer {gateway_key}"

    with httpx.Client(timeout=30) as client:
        health = client.get(f"{args.url.rstrip('/')}/v1/health")
        health.raise_for_status()
        print("Health:", health.json())

        response = client.post(
            f"{args.url.rstrip('/')}/v1/chat/completions",
            headers=headers,
            json={
                "model": "gateway-default",
                "messages": [{"role": "user", "content": args.message}],
                "temperature": 0.2,
            },
        )
        print("Status:", response.status_code)
        print(response.text)
        response.raise_for_status()


if __name__ == "__main__":
    main()
