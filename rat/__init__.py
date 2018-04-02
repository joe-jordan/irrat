from __future__ import print_function, division


class rat(object):
    """A type, like int(), float() and complex(), to represent rational numbers (fractions of ints) exactly."""

    class FactorisedInt(object):
        """An internal type for storing a number retaining both its value and a representation as prime factors."""

        def __init__(self, val=0, factors=None):
            """val can be any integer, or left out if 0 is desired."""
            if factors:
                # always copy the dictionary into a new object.
                self.factors = {k: v for k, v in factors.items()}
            elif val:
                self.factors = rat.FactorisedInt.factorise(abs(val))
            else:
                self.factors = {}

            # _value stores the sign of the number, as well as a cached form of the product of the factors.
            self.value = val

        def __repr__(self):
            return 'rat._FactorisedInt(' + repr(self.value) + ', ' + repr(self.factors) + ')'

        def copy(self):
            return rat.FactorisedInt(self.value, self.factors)

        @classmethod
        def factorise(cls, v):
            n = int(v)
            if v != n:
                print("Warning, inexact value", n, "computed from input value", repr(v), "in rationals library.")

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

        @classmethod
        def from_factors(cls, factors):
            value = 1
            for f, e in factors.items():
                value *= f**e

            return rat.FactorisedInt(value, factors)

        def __add__(self, other):
            if isinstance(other, rat.FactorisedInt):
                return rat.FactorisedInt(self.value + other.value)
            n = int(other)
            if n != other:
                print("Warning, inexact value", n, "computed from input value", repr(other), "in rationals library.")

            return rat.FactorisedInt(self.value + n)

        # addition is commutative
        __radd__ = __add__

        def __iadd__(self, other):
            if isinstance(other, rat.FactorisedInt):
                self.value += other.value
            else:
                n = int(other)
                if n != other:
                    print("Warning, inexact value", n, "computed from input value", repr(other),
                          "in rationals library.")

                self.value += n
            self.factors = rat.FactorisedInt.factorise(abs(self.value))

            return self

        def __sub__(self, other):
            if isinstance(other, rat.FactorisedInt):
                return rat.FactorisedInt(self.value - other.value)
            n = int(other)
            if n != other:
                print("Warning, inexact value", n, "computed from input value", repr(other), "in rationals library.")

            return rat.FactorisedInt(self.value - n)

        def __rsub__(self, other):
            if isinstance(other, rat.FactorisedInt):
                return rat.FactorisedInt(other.value - self.value)
            n = int(other)
            if n != other:
                print("Warning, inexact value", n, "computed from input value", repr(other), "in rationals library.")

            return rat.FactorisedInt(n - self.value)

        def __isub__(self, other):
            if isinstance(other, rat.FactorisedInt):
                self.value -= other.value
            else:
                n = int(other)
                if n != other:
                    print("Warning, inexact value", n, "computed from input value", repr(other),
                          "in rationals library.")

                self.value -= n
            self.factors = rat.FactorisedInt.factorise(abs(self.value))

            return self

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
                print("Warning, inexact value", n, "computed from input value", repr(other), "in rationals library.")

            return rat.FactorisedInt(self.value * n)

        # multiplication is commutative.
        __rmul__ = __mul__

        def __imul__(self, other):
            if not isinstance(other, rat.FactorisedInt):
                n = int(other)
                if n != other:
                    print("Warning, inexact value", n, "computed from input value", repr(other),
                          "in rationals library.")

                other = rat.FactorisedInt(n)

            for key, value in other.factors.items():
                try:
                    self.factors[key] += value
                except KeyError:
                    self.factors[key] = value

            self.value *= other.value

            return self

        def __div__(self, other):
            if other == 0:
                raise ZeroDivisionError()
            if self == 0:
                return self
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
                        denominator_factors[f] = abs(c)

                if denominator_factors:
                    return rat.from_factors(self.value, numerator_factors, other.value, denominator_factors)
                else:
                    return rat.FactorisedInt(self.value // other.value, numerator_factors)

            n = int(other)
            if n != other:
                print("Warning, inexact value", n, "computed from input value", repr(other), "in rationals library.")

            q, r = divmod(self.value, n)

            if r:
                return rat(self.value, n)

            return rat.FactorisedInt(q)

        # the whole point of rational types, is that the classic division/true division chasm is gone.
        __truediv__ = __div__

        def __rdiv__(self, other):
            if other == 0:
                raise ZeroDivisionError()
            if self == 0:
                return self
            if isinstance(other, rat.FactorisedInt):
                these_fs = set(self.factors.keys())
                other_fs = set(other.factors.keys())

                all_fs = these_fs.union(other_fs)
                numerator_factors = {}
                denominator_factors = {}

                for f in all_fs:
                    c = 0
                    try:
                        c -= self.factors[f]
                    except KeyError:
                        pass
                    try:
                        c += other.factors[f]
                    except KeyError:
                        pass

                    if c > 0:
                        numerator_factors[f] = c
                    elif c < 0:
                        denominator_factors[f] = abs(c)

                if denominator_factors:
                    return rat.from_factors(self.value, numerator_factors, other.value, denominator_factors)
                else:
                    return rat.FactorisedInt(other.value // self.value, numerator_factors)

            n = int(other)
            if n != other:
                print("Warning, inexact value", n, "computed from input value", repr(other), "in rationals library.")

            q, r = divmod(n, self.value)

            if r:
                return rat(n, self.value)

            return rat.FactorisedInt(q)

        __rtruediv__ = __rdiv__

        def __idiv__(self, other):
            if other == 0:
                raise ZeroDivisionError()
            if self == 0:
                return self
            if not isinstance(other, rat.FactorisedInt):
                n = int(other)
                if n != other:
                    print("Warning, inexact value", n, "computed from input value", repr(other),
                          "in rationals library.")

                other = rat.FactorisedInt(n)

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
                    denominator_factors[f] = abs(c)

            if denominator_factors:
                return rat.from_factors(self.value, numerator_factors, other.value, denominator_factors)
            else:
                self.value //= other.value
                self.factors = numerator_factors
                return self

        __itruediv__ = __idiv__

        def __pow__(self, e):
            copy = rat.FactorisedInt(self.value, self.factors)

            if isinstance(e, rat.FactorisedInt):
                e_as_int = e.value
            else:
                e_as_int = int(e)
                if e_as_int != e:
                    print("Warning, inexact value", e_as_int, "computed from input value", repr(e),
                          "in rationals library.")

            copy.value **= e_as_int
            for f in copy.factors.keys():
                copy.factors[f] *= e_as_int

            return copy

        def __rpow__(self, b):
            if self.value < 0:
                raise NotImplementedError("Should return an irrational, not implemented yet.")
            elif self.value == 0:
                # anything to the power 0 is 1.
                return rat.FactorisedInt(1)

            # do not modify the original object:
            if not isinstance(b, rat.FactorisedInt):
                b = rat.FactorisedInt(b)
            else:
                b = rat.FactorisedInt(b.value, b.factors)

            b.value **= self.value
            for f in b.factors.keys():
                b.factors[f] *= self.value

            return b

        def __ipow__(self, e):
            if isinstance(e, rat.FactorisedInt):
                e_as_int = e.value
            else:
                e_as_int = int(e)
                if e_as_int != e:
                    print("Warning, inexact value", e_as_int, "computed from input value", repr(e),
                          "in rationals library.")

            self.value **= e_as_int
            for f in self.factors.keys():
                self.factors[f] *= e_as_int

            return self

        def __eq__(self, other):
            if isinstance(other, rat.FactorisedInt):
                return self.value == other.value

            return self.value == other

        def __ne__(self, other):
            return not self.__eq__(other)

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

    @classmethod
    def from_factorised_ints(cls, num, denom):
        i = rat()
        i._numerator = num
        i._denominator = denom
        i._simplify()
        return i

    def __repr__(self):
        return 'rat(' + repr(self._numerator.value) + ', ' + repr(self._denominator.value) + ')'

    def __str__(self):
        # TODO call a arbitrary precision __format__ method with default values for a double with all its bits.
        return repr(self._numerator.value / self._denominator.value)

    def _simplify(self):
        if self._denominator.value < 0:
            self._numerator.value *= -1
            self._denominator.value *= -1

        nfs = self._numerator.factors
        dfs = self._denominator.factors

        common_factors = set(nfs.keys()).intersection(set(dfs.keys()))

        if len(common_factors) == len(nfs) and all([f in dfs and nfs[f] >= dfs[f] for f in nfs.keys()]):
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

    @classmethod
    def find_lowest_common_denominator(cls, self_denom_factors, other_denom_factors):
        """finds the lowest common denominator, and the numerator multipliers, for addition and subtraction.
        returns (lcd, self_numerator_multiplier, other_numerator_multiplier).
        """
        common_factors = set(other_denom_factors.keys()).union(set(self_denom_factors.keys()))

        # lowest common denominator
        lcd = {}

        # what to multiply the numerators by to convert the fractions to lcd. allow negatives until later.
        mul_self = {}

        for f in common_factors:
            lcd[f] = max([self_denom_factors[f], other_denom_factors[f]])
            mul_self[f] = other_denom_factors[f] - self_denom_factors[f]

        lcd = {f: e for f, e in lcd.items() if e != 0}

        mul_other = {f: abs(e) for f, e in mul_self.items() if e < 0}
        mul_self = {f: e for f, e in mul_self.items() if e > 0}

        # all that remains is to capture the values that these sets of factors represent, and build the rational.
        lcd = rat.FactorisedInt.from_factors(lcd)
        mul_other = rat.FactorisedInt.from_factors(mul_other)
        mul_self = rat.FactorisedInt.from_factors(mul_self)

        return lcd, mul_self, mul_other

    def __add__(self, other):
        if not isinstance(other, rat):
            # assume it is an integer (FactorisedInt will print a warning if it's a float.)
            new_numerator = self._numerator + other * self._denominator
            return rat.from_factorised_ints(new_numerator, self._denominator.copy())

        # (denominators are always +ve))
        if self._denominator.value == other._denominator.value:
            new_numerator = self._numerator + other._numerator
            return rat.from_factorised_ints(new_numerator, self._denominator.copy())

        # if not an integer, or the same denominator, then we must find the lowest common denominator:
        lcd, mul_self, mul_other = rat.find_lowest_common_denominator(self._denominator.factors,
                                                                      other._denominator.factors)

        new_numerator = self._numerator * mul_self + other._numerator * mul_other
        return rat.from_factorised_ints(new_numerator, lcd)

    # addition is commutative
    __radd__ = __add__

    def __iadd__(self, other):
        if not isinstance(other, rat):
            # assume it is an integer (FactorisedInt will print a warning if it's a float.)
            self._numerator += other * self._denominator
            self._simplify()
            return self

        # (denominators are always +ve))
        if self._denominator.value == other._denominator.value:
            self._numerator += other._numerator
            self._simplify()
            return self

        # if not an integer, or the same denominator, then we must find the lowest common denominator:
        lcd, mul_self, mul_other = rat.find_lowest_common_denominator(self._denominator.factors,
                                                                      other._denominator.factors)

        self._numerator *= mul_self
        self._numerator += other._numerator * mul_other
        self._denominator = lcd
        self._simplify()
        return self

    def __sub__(self, other):
        if not isinstance(other, rat):
            # assume it is an integer (FactorisedInt will print a warning if it's a float.)
            new_numerator = other * self._denominator - self._numerator
            return rat.from_factorised_ints(new_numerator, self._denominator.copy())

        # (denominators are always +ve))
        if self._denominator.value == other._denominator.value:
            new_numerator = other._numerator - self._numerator
            return rat.from_factorised_ints(new_numerator, self._denominator.copy())

        # if not an integer, or the same denominator, then we must find the lowest common denominator:
        lcd, mul_self, mul_other = rat.find_lowest_common_denominator(self._denominator.factors,
                                                                      other._denominator.factors)

        new_numerator = self._numerator * mul_self - other._numerator * mul_other
        return rat.from_factorised_ints(new_numerator, lcd)

    def __rsub__(self, other):
        if not isinstance(other, rat):
            # assume it is an integer (FactorisedInt will print a warning if it's a float.)
            new_numerator = other * self._denominator - self._numerator
            return rat.from_factorised_ints(new_numerator, self._denominator.copy())

        # (denominators are always +ve))
        if self._denominator.value == other._denominator.value:
            new_numerator = other._numerator - self._numerator
            return rat.from_factorised_ints(new_numerator, self._denominator.copy())

        # if not an integer, or the same denominator, then we must find the lowest common denominator:
        lcd, mul_self, mul_other = rat.find_lowest_common_denominator(self._denominator.factors,
                                                                      other._denominator.factors)

        new_numerator = other._numerator * mul_other - self._numerator * mul_self
        return rat.from_factorised_ints(new_numerator, lcd)

    def __isub__(self, other):
        if not isinstance(other, rat):
            # assume it is an integer (FactorisedInt will print a warning if it's a float.)
            self._numerator -= other * self._denominator
            self._simplify()
            return self

        # (denominators are always +ve))
        if self._denominator.value == other._denominator.value:
            self._numerator -= other._numerator
            self._simplify()
            return self

        # if not an integer, or the same denominator, then we must find the lowest common denominator:
        lcd, mul_self, mul_other = rat.find_lowest_common_denominator(self._denominator.factors,
                                                                      other._denominator.factors)

        self._numerator *= mul_self
        self._numerator -= other._numerator * mul_other
        self._denominator = lcd
        self._simplify()
        return self

    def __mul__(self, other):
        if isinstance(other, rat):
            new_num = self._numerator * other._numerator
            new_denom = self._denominator * other._denominator
            return rat.from_factorised_ints(new_num, new_denom)

        # will print a warning if other is not a sensible (integer) type.
        new_numerator = self._numerator * other
        return rat.from_factorised_ints(new_numerator, self._denominator.copy())

    # multiplication is commutative
    __rmul__ = __mul__

    def __imul__(self, other):
        if isinstance(other, rat):
            self._numerator *= other._numerator
            self._denominator *= other._denominator
        else:
            # will print a warning if other is not a sensible (integer) type.
            self._numerator *= other

        self._simplify()
        return self

    def __div__(self, other):
        if isinstance(other, rat):
            new_num = self._numerator * other._denominator
            new_denom = self._denominator * other._numerator
            return rat.from_factorised_ints(new_num, new_denom)

        # will print a warning if other is not a sensible (integer) type.
        new_denominator = self._denominator * other
        return rat.from_factorised_ints(self._numerator.copy(), new_denominator)

    __truediv__ = __div__

    def __rdiv__(self, other):
        if isinstance(other, rat):
            new_num = self._denominator * other._numerator
            new_denom = self._numerator * other._denominator
            return rat.from_factorised_ints(new_num, new_denom)

        # will print a warning if other is not a sensible (integer) type.
        new_numerator = self._denominator * other
        return rat.from_factorised_ints(new_numerator, self._numerator.copy())

    __rtruediv__ = __rdiv__

    def __idiv__(self, other):
        if isinstance(other, rat):
            self._numerator *= other._denominator
            self._denominator *= other._numerator
        else:
            # will print a warning if other is not a sensible (integer) type.
            self._denominator *= other

        self._simplify()
        return self

    __itruediv__ = __idiv__

    def __eq__(self, other):
        if isinstance(other, rat):
            # rational comparison (assumes that rats are pre-simplified).
            return self._numerator == other._numerator and self._denominator == other._denominator
        elif int(other) == other:
            # integer comparison
            return self._denominator == 1 and self._numerator == other
        else:
            # float comparison.
            return (self._numerator.value / self._denominator.value) == other

    def __ne__(self, other):
        return not self.__eq__(other)
