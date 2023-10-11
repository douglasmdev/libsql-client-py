import asyncio
import os
from time import perf_counter

from libsql_client import create_client

async def insert(client, t: str, s: str):
    return await client.execute(f"INSERT INTO {t} VALUES ('{s}')")

async def sync_demo(client):
    initial = perf_counter()
    for i in range(20):
        await insert(client, "sync", f"{i}")
    print(f"Sync code took {perf_counter() - initial} seconds to run.")

async def async_demo(client):
        initial = perf_counter()
        requests = [insert(client, "async", f"{i}") for i in range(20)]
        await asyncio.gather(*requests)
        print(f"Async code took {perf_counter() - initial} seconds to run.")

async def main():
    url = os.getenv("TURSO_URL", "")
    async with create_client(url) as client:
        await client.execute("CREATE TABLE IF NOT EXISTS sync (name TEXT)")
        await client.execute("CREATE TABLE IF NOT EXISTS async (name TEXT)")

        await sync_demo(client)
        await async_demo(client)



asyncio.run(main())