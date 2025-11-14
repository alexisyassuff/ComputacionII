#!/usr/bin/env python3

import argparse
import asyncio
import json
import aiohttp


async def main(server: str, url: str):
    async with aiohttp.ClientSession() as session:
        params = {"url": url}
        try:
            async with session.get(f"{server}/scrape", params=params, timeout=aiohttp.ClientTimeout(total=60)) as resp:
                text = await resp.text()
                try:
                    data = json.loads(text)
                except Exception:
                    print("Respuesta no JSON:", text)
                    return
                print(json.dumps(data, indent=2, ensure_ascii=False))
        except Exception as e:
            print("Error al conectar con servidor:", e)


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--server", default="http://127.0.0.1:8000", help="URL del servidor A")
    p.add_argument("--url", default="https://example.com", help="URL a scrapear")
    args = p.parse_args()
    asyncio.run(main(args.server, args.url))