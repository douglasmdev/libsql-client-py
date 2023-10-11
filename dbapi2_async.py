import asyncio
import logging
import os
from libsql_client.dbapi2 import connect
from time import perf_counter

REQUEST_COUNT = 1

async def insert(conn, t: str, s: str):
    return await conn.execute(f"INSERT INTO {t} VALUES ('{s}')")

async def sync_demo(conn):
    initial = perf_counter()
    for i in range(REQUEST_COUNT):
        await insert(conn, "sync", f"{i}")
    await conn.commit()
    print(f"Sync code took {perf_counter() - initial} seconds to run.")

async def async_demo(conn):
        initial = perf_counter()
        requests = [insert(conn, "async", f"{i}") for i in range(REQUEST_COUNT)]
        await asyncio.gather(*requests)
        await conn.commit()
        print(f"Async code took {perf_counter() - initial} seconds to run.")

async def main():
    logging.basicConfig(level=logging.DEBUG)
    url = os.getenv("TURSO_URL", "")
    conn = connect(url, uri=True)

    await conn.execute("CREATE TABLE IF NOT EXISTS dbapi2_sync (t TEXT)")
    await conn.execute("CREATE TABLE IF NOT EXISTS dbapi2_async (t TEXT)")

    await sync_demo(conn)
    await async_demo(conn)

    conn.close()

asyncio.run(main())