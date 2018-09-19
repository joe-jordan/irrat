import unittest
from irrat.factorize import prime_generator
from irrat.expression import Division


_FIRST_HUNDRED_PRIMES = list(prime_generator(546))


def product(*args):
    p = 1
    for i in args:
        p *= i
    return p


class DivisionExpressionTest(unittest.TestCase):
    def test_doesnt_factorize_large_primes_on_construction(self):
        # a fraction where the top and bottom share the 33rd prime as a factor.
        large_prime = _FIRST_HUNDRED_PRIMES[32]
        # multiply by an orthogonal set of smaller primes.
        expected_numerator = large_prime * 5 * 3 * 11
        expected_denominator = large_prime * 2 * 2 * 7

        expression = Division(expected_numerator, expected_denominator)

        actual_numerator, actual_denominator = expression.values

        self.assertEqual(expected_numerator, actual_numerator)
        self.assertEqual(expected_denominator, actual_denominator)

    def test_does_completely_factorize_out_smaller_primes_on_construction(self):
        common_factors = [2, 3, 7]
        expected_numerator = 5
        expected_denominator = 11

        expression = Division(product(expected_numerator, *common_factors),
                              product(expected_denominator, *common_factors))

        actual_numerator, actual_denominator = expression.values

        self.assertEqual(expected_numerator, actual_numerator)
        self.assertEqual(expected_denominator, actual_denominator)

    def test_does_completely_factorize_even_large_primes_on_request(self):
        # do not use more than 4 or so large primes here. The tests will take a very long time. (shouldn't use too much
        # RAM though. If they do, that's a bug!)
        # Note that this is particularly evil, as the product of a lot of very large primes like this is the worst-case
        # scenario for the sieve algorithm for factorization.
        common_factors = _FIRST_HUNDRED_PRIMES[96:]
        expected_numerator = 5
        expected_denominator = 11

        expression = Division(product(expected_numerator, *common_factors),
                              product(expected_denominator, *common_factors))

        # first of all, they should be unequal:
        actual_numerator, actual_denominator = expression.values

        self.assertNotEqual(expected_numerator, actual_numerator)
        self.assertNotEqual(expected_denominator, actual_denominator)

        expression.fully_simplify()

        # then, they should be fully cancelled.
        actual_numerator, actual_denominator = expression.values

        self.assertEqual(expected_numerator, actual_numerator)
        self.assertEqual(expected_denominator, actual_denominator)
