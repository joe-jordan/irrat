from __future__ import print_function, division


class rat(object):
    """A type, like int(), float() and complex(), to represent rational numbers (fractions) exactly."""

    class FactorisedInt(object):
        """An internal type for storing a number retaining both its value and a representation as prime factors."""

        def __init__(self, val=0, factors=None):
            """val can be any integer, or left out if 0 is desired."""
            if factors:
                self.factors = factors
            elif val:
                self.factors = rat.FactorisedInt.factorise(abs(val))
            else:
                self.factors = {}
                val = 0

            # _value stores the sign of the number, as well as a cached form of the product of the factors.
            self.value = val

        def __repr__(self):
            return 'rat._FactorisedInt(' + repr(self.value) + ', ' + repr(self.factors) + ')'

        @classmethod
        def factorise(cls, v):
            n = int(v)
            if v != n:
                print("Warning, inexact value", n, "computed from input value", v, "in rationals library.")

            factors = {}

            while n % 2 == 0:
                try:
                    factors[2] += 1
                except KeyError:
                    factors[2] = 1
                n >>= 1

            f = 3
            while n > 1:
                while n % f == 0:
                    try:
                        factors[f] += 1
                    except KeyError:
                        factors[f] = 1
                    n //= f
                f += 2
                if f*f > n:
                    if n > 1:
                        # the remaining number must be prime, and is the last factor:
                        factors[n] = 1
                    break
            return factors

        def __add__(self, other):
            if isinstance(other, rat.FactorisedInt):
                return rat.FactorisedInt(self.value + other.value)
            n = int(other)
            if n != other:
                print("Warning, inexact value", n, "computed from input value", other, "in rationals library.")

            return rat.FactorisedInt(self.value + n)

        def __sub__(self, other):
            if isinstance(other, rat.FactorisedInt):
                return rat.FactorisedInt(self.value - other.value)
            n = int(other)
            if n != other:
                print("Warning, inexact value", n, "computed from input value", other, "in rationals library.")

            return rat.FactorisedInt(self.value - n)

        def __mul__(self, other):
            if isinstance(other, rat.FactorisedInt):
                these_fs = set(self.factors.keys())
                other_fs = set(other.factors.keys())

                all_fs = these_fs.union(other_fs)
                new_factors = {}

                for f in all_fs:
                    c = 0
                    try:
                        c += self.factors[f]
                    except KeyError:
                        pass
                    try:
                        c += other.factors[f]
                    except KeyError:
                        pass

                    assert c, "found a factor that shouldn't exist..."

                    new_factors[f] = c

                return rat.FactorisedInt(self.value * other.value, new_factors)

            n = int(other)
            if n != other:
                print("Warning, inexact value", n, "computed from input value", other, "in rationals library.")

            return rat.FactorisedInt(self.value * n)

        def __div__(self, other):
            if isinstance(other, rat.FactorisedInt):
                these_fs = set(self.factors.keys())
                other_fs = set(other.factors.keys())

                all_fs = these_fs.union(other_fs)
                numerator_factors = {}
                denominator_factors = {}

                for f in all_fs:
                    c = 0
                    try:
                        c += self.factors[f]
                    except KeyError:
                        pass
                    try:
                        c -= other.factors[f]
                    except KeyError:
                        pass

                    if c > 0:
                        numerator_factors[f] = c
                    elif c < 0:
                        denominator_factors[f] = c

                if denominator_factors:
                    return rat.from_factors(self.value, numerator_factors, other.value, denominator_factors)
                else:
                    return rat.FactorisedInt(self.value // other.value, numerator_factors)

            n = int(other)
            if n != other:
                print("Warning, inexact value", n, "computed from input value", other, "in rationals library.")

            q, r = divmod(self.value, n)

            if r:
                return rat(self.value, n)

            return rat.FactorisedInt(q)

    def __init__(self, *args):
        """rat(numerator, denominator=0), where arguments should be integers for best results (will continue but
        print warnings if floats are passed, and they will be approximated.)"""
        if args:
            self._numerator = rat.FactorisedInt(args[0])
            try:
                self._denominator = rat.FactorisedInt(args[1])
            except IndexError:
                self._denominator = rat.FactorisedInt(1)
        else:
            self._numerator = rat.FactorisedInt()
            self._denominator = rat.FactorisedInt(1)

        self._simplify()

    @classmethod
    def from_factors(cls, num, num_factors, denom, denom_factors):
        i = rat()
        i._numerator = rat.FactorisedInt(num, num_factors)
        i._denominator = rat.FactorisedInt(denom, denom_factors)
        i._simplify()
        return i

    def __repr__(self):
        return 'rat(' + repr(self._numerator.value) + ', ' + repr(self._denominator.value) + ')'

    def _simplify(self):
        if self._numerator.value < 0 and self._denominator.value < 0:
            self._numerator.value *= -1
            self._denominator.value *= -1

        nfs = self._numerator.factors
        dfs = self._denominator.factors

        common_factors = set(nfs.keys()).intersection(set(dfs.keys()))

        if len(common_factors) == len(nfs) and all([f in dfs and nfs[f] > dfs for f in nfs.keys()]):
            # this number is an integer.
            self._numerator = self._numerator / self._denominator
            self._denominator = rat.FactorisedInt(1)
        elif len(common_factors):
            # we can cancel some common factors.
            for f in common_factors:
                if nfs[f] > dfs[f]:
                    # completely cancel this prime from the denominator.
                    c = dfs[f]
                    del dfs[f]
                    self._denominator.value //= f**c

                    nfs[f] -= c
                    self._numerator.value //= f**c
                elif dfs[f] > nfs[f]:
                    # completely cancel this prime from the numerator.
                    c = nfs[f]
                    del nfs[f]
                    self._numerator.value //= f**c

                    dfs[f] -= c
                    self._denominator.value //= f**c
                else:
                    # completely cancel this prime from both terms.
                    c = dfs[f]
                    assert c == nfs[f]

                    c = nfs[f]
                    del nfs[f]
                    self._numerator.value //= f**c

                    c = dfs[f]
                    del dfs[f]
                    self._denominator.value //= f**c

