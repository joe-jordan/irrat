"""Functions for factorising integers and associated things."""
import math
from collections import defaultdict


def _to_sieve_index(i):
    """3 => 0
    5 => 1
    7 => 2
    9 => 3"""
    return (i - 3) // 2


def prime_generator(limit):
    limit = int(math.ceil(limit))
    n = 2
    if n < limit:
        yield n
    # use a list, not a dict (saves a lot of memory).
    is_prime = [True for _ in range(_to_sieve_index(limit) + 1)]
    n = 3
    while n < limit:
        try:
            if not is_prime[_to_sieve_index(n)]:
                continue
            yield n
            # only look at odd multiples - even ones yield a spurious sieve index.
            m = n * 3
            while m < limit:
                is_prime[_to_sieve_index(m)] = False
                m += n * 2
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
