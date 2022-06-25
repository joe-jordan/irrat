from abc import abstractmethod
import unittest
from irrat.factorize import CautiousPrimeGenerator, cautious_factorize, prime_generator, factorize
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


class PrimeGeneratorTests:
    # set this higher if you want to burn some cycles.
    LARGE_LIMIT = 10000

    def assertIsPrime(self, n):
        self.assertTrue(_is_prime(n), f"{n} is not prime.")

    @abstractmethod
    def prime_generator(self, limit):
        """Since we have multiple prime generator implementations, we abstract which one we're
        using here."""
        raise NotImplementedError()

    @abstractmethod
    def assertTrue(self, test, message=""):
        raise NotImplementedError()

    @abstractmethod
    def assertEqual(self, a, b, message=""):
        raise NotImplementedError()

    @abstractmethod
    def assertNotIn(self, item, collection, message=""):
        raise NotImplementedError()

    def test_obvious_primes(self):
        expected_primes = [2, 3, 5, 7, 11, 13, 17, 19]
        actual_primes = list(self.prime_generator(20))

        self.assertEqual(expected_primes, actual_primes)

    def test_all_are_prime(self):
        for p in self.prime_generator(self.LARGE_LIMIT):
            self.assertIsPrime(p)

    def test_no_primes_are_missing(self):
        actual_primes = list(self.prime_generator(self.LARGE_LIMIT))
        for i in range(1, self.LARGE_LIMIT):
            if _is_prime(i):
                self.assertIn(i, actual_primes)
            else:
                self.assertNotIn(i, actual_primes)


class DirectPrimeGeneratorTest(PrimeGeneratorTests, unittest.TestCase):
    def prime_generator(self, limit):
        """Since we have multiple prime generator implementations, we abstract which one we're
        using here."""
        return prime_generator(limit)


class CautiousPrimeGeneratorDirectTest(PrimeGeneratorTests, unittest.TestCase):
    def prime_generator(self, limit):
        gen = CautiousPrimeGenerator(limit)
        return iter(gen)


class CautiousPrimeGeneratorRampingUpTest(PrimeGeneratorTests, unittest.TestCase):
    def prime_generator(self, limit):
        tmp_limit = limit // 3
        gen = CautiousPrimeGenerator(tmp_limit)
        for prime in gen:
            yield prime
        # Raised StopIteration, now we can increase the limit:
        gen.increase_limit(limit)
        for higher_prime in gen:
            yield higher_prime


class FactorizeTest:
    @abstractmethod
    def factorize(self, n):
        raise NotImplementedError()

    @abstractmethod
    def assertTrue(self, test, message=""):
        raise NotImplementedError()

    @abstractmethod
    def assertEqual(self, a, b, message=""):
        raise NotImplementedError()

    def test_20(self):
        expected_factors = {
            2: 2,
            5: 1,
        }
        actual_factors = factorize(20)
        self.assertEqual(expected_factors, actual_factors)

    def test_some_numbers(self):
        nums = []
        for _ in range(20):
            nums.append(random.randint(2, 100000))
        for n in nums:
            factors = factorize(n)
            product = 1
            for p, c in factors.items():
                self.assertTrue(_is_prime(p))
                product *= p**c
            self.assertEqual(product, n)


class DirectFactorizeTests(FactorizeTest, unittest.TestCase):
    def factorize(self, n):
        return factorize(n)


class CautiousFactorizeTests(FactorizeTest, unittest.TestCase):
    def factorize(self, n):
        return cautious_factorize(n)
