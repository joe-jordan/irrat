import unittest
from irrat.factorize import prime_generator, factorize
import random


def _is_prime(n):
    """a naive method which is obviously correct."""
    if n == 1:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    for i in range(3, n - 1, 2):
        if n % i == 0:
            return False
    return True


class PrimeTests(unittest.TestCase):
    # set this higher if you want to burn some cycles.
    LARGE_LIMIT = 10000

    def assertIsPrime(self, n):
        self.assertTrue(_is_prime(n))

    def test_obvious_primes(self):
        expected_primes = [2, 3, 5, 7, 11, 13, 17, 19]
        actual_primes = list(prime_generator(20))

        self.assertEqual(expected_primes, actual_primes)

    def test_all_are_prime(self):
        for p in prime_generator(self.LARGE_LIMIT):
            self.assertIsPrime(p)

    def test_no_primes_are_missing(self):
        actual_primes = list(prime_generator(self.LARGE_LIMIT))
        for i in range(1, self.LARGE_LIMIT):
            if _is_prime(i):
                self.assertIn(i, actual_primes)
            else:
                self.assertNotIn(i, actual_primes)


class FactorizeTest(unittest.TestCase):
    def test_20(self):
        expected_factors = {
            2: 2,
            5: 1,
        }
        actual_factors = factorize(20)
        self.assertEqual(expected_factors, actual_factors)

    def test_some_numbers(self):
        nums = []
        for i in range(20):
            nums.append(random.randint(2, 100000))
        for n in nums:
            factors = factorize(n)
            product = 1
            for p in factors.keys():
                self.assertTrue(_is_prime(p))
                product *= (p ** factors[p])
            self.assertEqual(product, n)

