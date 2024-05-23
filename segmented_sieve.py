# https://www.geeksforgeeks.org/python-program-for-sieve-of-eratosthenes/

import math
import array
from functools import lru_cache


@lru_cache(maxsize=None)
def segmented_sieve(limit):
    primes = []
    sieve_size = int(math.sqrt(limit)) + 1
    sieve = array.array('B', [True]) * sieve_size
    sieve[0] = False
    sieve[1] = False

    # Skip even numbers in the sieve
    for i in range(4, sieve_size, 2):
        sieve[i] = False

    # Wheel factorization
    wheel = [2, 3, 5]
    wheel_idx = 0
    wheel_skip = [1, 2, 4, 2, 4, 6, 2, 6]
    wheel_skip_idx = 0

    for i in range(7, sieve_size, wheel[wheel_idx]):
        if sieve[i]:
            primes.append(i)
            for j in range(i * i, sieve_size, i):
                sieve[j] = False

        wheel_skip_idx += 1
        if wheel_skip_idx == len(wheel_skip):
            wheel_skip_idx = 0
            wheel_idx += 1
            if wheel_idx == len(wheel):
                wheel_idx = 0

    low = sieve_size
    high = 2 * sieve_size

    while low < limit:
        if high > limit:
            high = limit

        segment = array.array('B', [True]) * (high - low)

        for prime in primes:
            start = (low // prime) * prime
            if start < low:
                start += prime
            for j in range(start, high, prime):
                segment[j - low] = False

        for i in range(low, high):
            if segment[i - low]:
                primes.append(i)

        low += sieve_size
        high += sieve_size

    return len(primes)


limit = 1_000_000
count = segmented_sieve(limit)
print("Number of primes up to", limit, ":", count)
