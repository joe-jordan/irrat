"""Types for representing expressions (of which rationals and irrationals are examples)
For internal use by the public classes of the library."""
from abc import ABC, abstractmethod
from operator import invert

from irrat.factorize import prime_generator, factorize, cautious_factorize


class Expression(ABC):
    """Expression: an Abstract Base Class representing any form of delayed computation, which can
    be approximated and evaulated later."""

    @property
    @abstractmethod
    def approximation(self):
        """Returns an inexact approximation of a computation (e.g. a floating point representation)
        Intended for > and < comparisons, but not suitable for == !="""
        raise NotImplementedError()

    @abstractmethod
    def evaluate(self, target_type=float, precision=50):
        """evaluate(float) => approximation()
        evaluate(str, N) => '(floating point or scientific form to N significant figures.)'"""
        raise NotImplementedError()


class Division(Expression):
    def __init__(self, numerator, denominator):
        super(Division, self).__init__()
        if denominator < 0:
            denominator *= -1
            numerator *= -1
        self.values = (numerator, denominator)
        self._fully_simplified = False
        self._quick_simplify()

    def evaluate(self, target_type=float, precision=50):
        if target_type is float:
            a, b = self.values
            return a / b
        else:
            self.fully_simplify()
            # TODO string formatting to arbitrary precision.
            raise NotImplementedError()

    @property
    def approximation(self):
        # Just return the float result from normal division.
        return self.values[0] / self.values[1]

    def _quick_simplify(self, prime_limit=23):
        if self._fully_simplified:
            return
        a, b = self.values
        # already an integer (or inverted integer):
        if abs(a) == 1 or b == 1:
            return

        # trivially an integer:
        if a % b == 0:
            a = a // b
            b = 1
        else:
            # perform a quick, lazy simplification that will work on many fractions.
            for prime in prime_generator(prime_limit):
                while a % prime == 0 and b % prime == 0:
                    a //= prime
                    b //= prime

        self.values = (a, b)

    def fully_simplify(self):
        if self._fully_simplified:
            return
        self._quick_simplify()
        a, b = self.values

        # Lots of code here assumes +ve numbers.
        neg = a < 0
        a = abs(a)

        if a == 1 or b == 1:
            return

        # We want to avoid factorizing large numbers, as that's very intensive.
        # We choose to factorize the smaller of the two numbers, but if it's still
        # very large then we'll just try to find the first factor, and divide.

        inverted = False
        if a > b:
            a, b = b, a
            inverted = True

        # a is smaller, so we try our best to factorize it:
        if a < 10000**2:
            a_factors = factorize(a)
        else:
            a_factors = cautious_factorize(a)

        # TODO don't factorize b, just % each of a's factors to see if common.

        common_factors = filter(lambda f: b % f == 0, a_factors.keys())

        for f in common_factors:
            while b % f == 0 and a_factors[f] > 0:
                a //= f
                b //= f
                a_factors[f] -= 1

        if inverted:
            a, b = b, a

        self.values = (-a, b) if neg else (a, b)
        self._fully_simplified = True

    @property
    def numerator(self):
        return self.values[0]

    @property
    def denominator(self):
        return self.values[1]
