from __future__ import division
from irrat.factorize import prime_generator, factorize


class Expression(object):
    def evaluate(self):
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

    def evaluate(self, target_type=float, precision_sf=3):

        if target_type is float:
            a, b = self.values
            return a / b
        else:
            self.fully_simplify()
            # TODO string formatting to arbitrary precision.
            raise NotImplementedError()

    def _quick_simplify(self):
        if self._fully_simplified:
            return
        a, b = self.values
        # already an integer:
        if abs(a) == 1 or b == 1:
            return

        # trivially an integer:
        if a % b == 0:
            a = a // b
            b = 1
        else:
            # perform a quick, lazy simplification that will work on many fractions.
            for prime in prime_generator(23):
                while a % prime == 0 and b % prime == 0:
                    a //= prime
                    b //= prime

        self.values = (a, b)

    def fully_simplify(self):
        if self._fully_simplified:
            return
        self._quick_simplify()
        a, b = self.values
        if abs(a) == 1 or b == 1:
            return

        a_factors = factorize(a)
        b_factors = factorize(b)

        common_factors = {
            p: min(a_factors[p], b_factors[p])
            for p in set(a_factors.keys()) & set(b_factors.keys())
        }

        for p, order in common_factors.items():
            common_factor = p ** order
            a //= common_factor
            b //= common_factor

        self.values = (a, b)
        self._fully_simplified = True

    @property
    def numerator(self):
        return self.values[0]

    @property
    def denominator(self):
        return self.values[1]
