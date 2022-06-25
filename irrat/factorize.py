"""Functions for factorising integers and associated things."""
import math
from collections import defaultdict


def _to_sieve_index(i):
    """3 => 0
    5 => 1
    7 => 2
    9 => 3"""
    return (i - 3) // 2


def _reverse_sieve_index(i):
    """0 => 3
    1 => 5
    2 => 7
    3 => 9"""
    return (i * 2) + 3


def prime_generator(limit):
    """Generator function which yields primes up to a limit. Creates a list of size limit / 2."""
    limit = int(math.ceil(limit))
    n = 2
    if n <= limit:
        yield n
    # use a list, not a dict (saves a lot of memory).
    is_prime = [True] * (_to_sieve_index(limit) + 1)
    n = 3
    while n <= limit:
        try:
            if not is_prime[_to_sieve_index(n)]:
                continue
            yield n
            # only look at odd multiples - even ones yield a spurious sieve index.
            m = n * 3
            while m <= limit:
                is_prime[_to_sieve_index(m)] = False
                m += n * 2
        finally:
            n += 2


def factorize(n):
    """Fast factorize for small numbers. Uses a list of length sqrt(n)/2 during computation."""
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


class CautiousPrimeGenerator:
    """Generator class for primes, which yields them up to a limit and then raises StopIteration.
    Note: you can call increase_limit(larger), and then resume iterating to get higher primes,
    gradually increasing the RAM you are using. Suitable for factorizing larger numbers."""

    def __init__(self, limit):
        self.limit = int(math.ceil(limit))
        self.is_prime = [True] * (_to_sieve_index(limit) + 1)
        self.last_prime = None

    def __next__(self):
        if self.last_prime is None:
            if 2 < self.limit:
                self.last_prime = 2
                return self.last_prime

        old_last_prime = self.last_prime

        if self.last_prime == 2:
            self.last_prime = 3
        else:
            self.last_prime += 2

        while self.last_prime <= self.limit:

            if not self.is_prime[_to_sieve_index(self.last_prime)]:
                # This is equivalent to returning a prime - we know that we reliably excluded this
                # number. We can start from this point after an increased limit.
                old_last_prime = self.last_prime
                self.last_prime += 2
                continue
            # is a prime, mark off the odd multiples and return it.
            m = self.last_prime * 3
            while m <= self.limit:
                self.is_prime[_to_sieve_index(m)] = False
                m += self.last_prime * 2

            return self.last_prime

        # hmm. last_prime should represent the last one we actually returned, so we pick up
        # correctly after an increased limit.
        self.last_prime = old_last_prime

        # We didn't return a prime and finished the while loop: we're done.
        # Note, you can call increate_limit(), and then call next() again.
        raise StopIteration()

    def __iter__(self):
        return self

    def increase_limit(self, new_limit):
        if new_limit <= self.limit:
            return
        new_limit = int(math.ceil(new_limit))
        self._append_new_prime_candidates(new_limit)
        self.limit = new_limit

    def _append_new_prime_candidates(self, new_limit):
        known_primes = self.is_prime
        extra_entries = [True] * ((_to_sieve_index(new_limit) + 1) - len(self.is_prime))
        self.is_prime = known_primes + extra_entries
        first_new_number = _reverse_sieve_index(len(known_primes))

        # We must mark off known-not-primes as if they were part of the array so far.
        # Loop over each known prime:
        for p in map(
            lambda t: _reverse_sieve_index(t[0]), filter(lambda t: t[1], enumerate(known_primes))
        ):
            # compute (lowest multiple of p) >= first_new_number
            multiple = first_new_number // p

            # If not an exact multiple, then we have already marked the floor as prime.
            if first_new_number % p != 0:
                multiple += 1

            # If an even multiple, then we'll get a spurious sieve index, so move to the next odd
            # one.
            if multiple % 2 == 0:
                multiple += 1

            # Usual marking algorithm starting at multiple.
            m = p * multiple
            while m < new_limit:
                self.is_prime[_to_sieve_index(m)] = False
                m += p * 2


def cautious_factorize(n):
    """A slower factorize algorithm for large n.
    Uses the same algorthm as factorize but only generates the primes in batches, and applies
    division to the number liberally before increasing the n in the list."""
    if not isinstance(n, int):
        raise NotImplementedError()

    if n < 10000**2:
        # very low resource situation assumed, generate 1/10 of the range of possible primes at a
        # time.
        upper = math.sqrt(n)
        increment = upper / 5
        lim_sequence = [increment * i for i in range(1, 6)]
    else:
        # escalate by orders of magnitude so that we do hit all ranges, but only allocate lots of
        # RAM if we really need it.
        upper = math.sqrt(n)
        lim_sequence = []
        i = 1000
        while i < upper:
            lim_sequence.append(i)
            i *= 10
        lim_sequence.append(upper)

    # Note that in both cases, we hope to avoid actually calling increase_limit for _every_ item
    # in lim_sequence. As soon as we find a prime, we can divide it out and find a new, smaller
    # upper, and if this is less than our current limit then we need never increase.

    tmp = n
    factors = defaultdict(lambda: 0)

    current_limit = 0
    prime_escalator = CautiousPrimeGenerator(current_limit)

    # tmp should slowly decrease as we find factors and divide them out.
    # Once tmp is low enough, we can break out.

    while math.sqrt(tmp) > current_limit and lim_sequence:
        current_limit = lim_sequence.pop(0)
        prime_escalator.increase_limit(current_limit)

        for p in prime_escalator:
            while tmp % p == 0:
                tmp //= p
                factors[p] += 1
            if tmp < p:
                # Short cut, no need to compute higher primes.
                break

    if tmp != 1:
        factors[tmp] += 1
    return dict(factors)
