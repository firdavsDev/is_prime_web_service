"""
Web Service:
    - Implement a RESTful API that receives a number and returns the number of prime numbers that exist up to and including that number.
    - The API should have two endpoints:
        - PUT /number?v=100
        - GET /number?timeout=1000
    - The PUT endpoint should accept a number as a query parameter and return a 200 status code.
    - The GET endpoint should return a JSON object with the number and the count of prime numbers that exist up to and including that number.
    - The API should be able to handle multiple requests at the same time.
    - The API should be able to handle a timeout query parameter on the GET endpoint. If the timeout is reached, the API should return a 404 status code.
    - The API should be able to handle large numbers efficiently.
    - The API should be implemented using asyncio.
    - The API should be implemented using aiohttp.

Example:
    PUT /number?v=100
    GET /number?timeout=1000
    {
        "v": 100,
        "count": 25
    }
"""


import asyncio
from concurrent.futures import ThreadPoolExecutor
import sys
from math import sqrt

from aiohttp import web
# from async_lru import alru_cache #pip install async_lru

executor = ThreadPoolExecutor()


class AsyncQueue:
    def __init__(self):
        self._queue = asyncio.Queue()

    async def put(self, item):
        await self._queue.put(item)

    async def get(self, timeout=None):
        if timeout:
            try:
                return await asyncio.wait_for(self._queue.get(), timeout)
            except asyncio.TimeoutError:
                return None
        return await self._queue.get()


# @alru_cache(maxsize=None)
async def count_primes(v):
    loop = asyncio.get_running_loop()
    count = await loop.run_in_executor(executor, count_primes_sync, v)
    return count


def count_primes_sync(v):
    """
    Sieve of Eratosthenes 
    
    :param v: int
    """
    sieve = [True] * (v + 1)
    sieve[0:2] = [False, False]
    for i in range(2, int(sqrt(v)) + 1):
        if sieve[i]:
            for j in range(i * i, v + 1, i):
                sieve[j] = False

    return sum(sieve)


result_queue = AsyncQueue()


async def calculate_primes(v):
    count = await count_primes(v)
    await result_queue.put({"v": v, "count": count})


async def handle_put(request):
    v = request.query.get('v')
    if not v or not v.isdigit() or int(v) <= 2:
        return web.Response(status=400)

    v = int(v)
    asyncio.create_task(calculate_primes(v))
    return web.Response(status=200)


async def handle_get(request):
    timeout = request.query.get('timeout')
    timeout = int(timeout) if timeout and timeout.isdigit() else None

    result = await result_queue.get(timeout)
    if result is None:
        return web.Response(status=404)

    return web.json_response(result)


def create_app():
    app = web.Application()
    app.router.add_put('/number', handle_put)
    app.router.add_get('/number', handle_get)
    return app


def main(port: int = 5000):
    app = create_app()
    web.run_app(app, port=port)


if __name__ == '__main__':
    port = sys.argv[1] if len(sys.argv) > 1 else 5000
    main(port=int(port))
