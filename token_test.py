#!/usr/bin/env python3
import os
from pathlib import Path
from kiteconnect import KiteConnect

def main():
    api_key = os.getenv("KITE_API_KEY") or input("KITE_API_KEY: ").strip()
    api_secret = os.getenv("KITE_API_SECRET") or input("KITE_API_SECRET: ").strip()

    kite = KiteConnect(api_key=api_key)
    login_url = kite.login_url()
    print("Open this login URL, complete sign-in, then paste request_token from the redirected URL:")
    print(login_url)

    request_token = input("request_token: ").strip()
    data = kite.generate_session(request_token, api_secret=api_secret)
    access_token = data["access_token"]
    refresh_token = data.get("refresh_token")

    print(f"\nACCESS_TOKEN={access_token}")
    if refresh_token:
        print(f"REFRESH_TOKEN={refresh_token}")

    # Optional: persist to .env for Docker/env_file workflows
    env_path = Path(".env")
    existing = {}
    if env_path.exists():
        for line in env_path.read_text().splitlines():
            if "=" in line and not line.strip().startswith("#"):
                k, v = line.split("=", 1)
                existing[k] = v
    existing["KITE_API_KEY"] = api_key
    existing["KITE_API_SECRET"] = api_secret
    existing["KITE_ACCESS_TOKEN"] = access_token
    if refresh_token:
        existing["KITE_REFRESH_TOKEN"] = refresh_token
    env_path.write_text("\n".join(f"{k}={v}" for k, v in existing.items()) + "\n")
    print(f"\nWrote tokens to {env_path.resolve()}")

if __name__ == "__main__":
    main()
