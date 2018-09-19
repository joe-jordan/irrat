from __future__ import division
import math
from collections import defaultdict


def prime_generator(limit):
    limit = int(math.ceil(limit))
    n = 2
    if n < limit:
        yield n
    is_prime = {i: True for i in range(3, limit, 2)}
    n = 3
    while n < limit:
        try:
            if not is_prime[n]:
                continue
            yield n
            m = n * 2
            while m < limit:
                is_prime[m] = False
                m += n
        finally:
            n += 2


def factorize(n):
    if not isinstance(n, int):
        raise NotImplementedError()
    tmp = n
    factors = defaultdict(lambda: 0)
    for p in prime_generator(math.sqrt(n)):
        while tmp % p == 0:
            tmp //= p
            factors[p] += 1
    if tmp != 1:
        factors[tmp] += 1
    return dict(factors)