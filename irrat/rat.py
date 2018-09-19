from __future__ import print_function, division
from irrat.expression import Division


class rat(object):
    """A type, like int(), float() and complex(), to represent rational numbers (fractions of ints) exactly."""

    def __init__(self, *args):
        """rat(numerator, denominator=0), where arguments should be integers for best results (will continue but
        print warnings if floats are passed, and they will be approximated.)"""
        if args:
            numerator = args[0]
            try:
                denominator = args[1]
            except IndexError:
                denominator = 1
        else:
            numerator = 0
            denominator = 1

        if not isinstance(numerator, int):
            if not isinstance(numerator, float):
                raise NotImplementedError("can't convert non-numeric object (%r) to rational." % numerator)
            if numerator == 0.:
                numerator = 0
            else:
                numerator, denominator_factor = self._from_float(numerator)
                denominator *= denominator_factor

        self.expression = Division(numerator, denominator)

    @staticmethod
    def _from_float(f):
        denominator_factor = 1
        # math.frepr doesn't give me anything I can work with here (namely, two integers), so just print to
        # decimal string and use that. In Python, this is often rounded to the literal the user typed anyway.
        as_string = repr(f)
        if 'e' in as_string:
            mantissa, exponent = as_string.split('e')
        else:
            mantissa = as_string
            exponent = '0'
        exponent = int(exponent)
        if '.' in mantissa:
            pre, post = mantissa.split('.')
            exponent -= len(post)
            mantissa = pre + post
        mantissa = int(mantissa)
        if exponent >= 0:
            mantissa *= 10 ** exponent
        else:
            denominator_factor *= 10 ** abs(exponent)
        return mantissa, denominator_factor

    def __repr__(self):
        self.expression.fully_simplify()
        return 'rat(' + repr(self.expression.numerator.value) + ', ' + repr(self.expression.denominator.value) + ')'

    def __str__(self):
        # when we have implemented this:
        # return self.expression.evaluate(target_type=str, precision_sf=50)
        # for now, just convert to float:
        return str(self.expression.evaluate())

    def __add__(self, other):
        if isinstance(other, int):
            # assume it is an integer (FactorisedInt will print a warning if it's a float.)
            new_numerator = self.expression.numerator + other * self.expression.denominator
            return rat(new_numerator, self.expression.denominator)
        elif not isinstance(other, rat):
            # do our best type conversion!
            other = rat(other)

        # (denominators are always +ve))
        if self.expression.denominator == other.expression.denominator:
            new_numerator = self.expression.numerator + other.expression.numerator
            return rat(new_numerator, self.expression.denominator)

        # if not an integer, or the same denominator, we compute the relevant numerator and denominator and let Division
        # simplify it, flagging that we'd like it to work a little harder than usual in this case:
        new_numerator = self.expression.numerator * other.expression.denominator + \
                        other.expression.numerator * self.expression.denominator
        new_denominator = self.expression.denominator * other.expression.denominator
        new_expression = Division(new_numerator, new_denominator)
        new_expression.fully_simplify()
        new_rat = rat()
        new_rat.expression = new_expression
        return new_rat

    # addition is commutative
    __radd__ = __add__

    def __iadd__(self, other):
        # in order to behave like the other numeric types, we make rat immutable, and return a new one in += cases:
        return self + other

    def __sub__(self, other):
        if isinstance(other, int):
            new_numerator = self.expression.numerator - other * self.expression.denominator
            return rat(new_numerator, self.expression.denominator)
        elif not isinstance(other, rat):
            # do our best type conversion!
            other = rat(other)

        # (denominators are always +ve))
        if self.expression.denominator == other.expression.denominator:
            new_numerator = self.expression.numerator - other.expression.numerator
            return rat(new_numerator, self.expression.denominator)

        # if not an integer, or the same denominator, we compute the relevant numerator and denominator and let Division
        # simplify it, flagging that we'd like it to work a little harder than usual in this case:
        new_numerator = self.expression.numerator * other.expression.denominator - \
                        other.expression.numerator * self.expression.denominator
        new_denominator = self.expression.denominator * other.expression.denominator
        new_expression = Division(new_numerator, new_denominator)
        new_expression.fully_simplify()
        new_rat = rat()
        new_rat.expression = new_expression
        return new_rat

    def __rsub__(self, other):
        tmp = self.__sub__(other)
        return tmp * -1

    def __isub__(self, other):
        # in order to behave like the other numeric types, we make rat immutable, and return a new one in -= cases:
        return self - other

    def __mul__(self, other):
        if isinstance(other, int):
            new_numerator = self.expression.numerator * other
            return rat(new_numerator, self.expression.denominator)
        elif not isinstance(other, rat):
            # do our best type conversion!
            other = rat(other)

        new_num = self.expression.numerator * other.expression.numerator
        new_denom = self.expression.denominator * other.expression.denominator
        return rat(new_num, new_denom)

    # multiplication is commutative
    __rmul__ = __mul__

    def __imul__(self, other):
        # in order to behave like the other numeric types, we make rat immutable, and return a new one in *= cases:
        return self * other

    def __div__(self, other):
        if isinstance(other, int):
            new_denominator = self.expression.denominator * other
            return rat(self.expression.numerator, new_denominator)
        elif not isinstance(other, rat):
            # do our best type conversion!
            other = rat(other)

        new_num = self.expression.numerator * other.expression.denominator
        new_denom = self.expression.denominator * other.expression.numerator
        return rat(new_num, new_denom)

    __truediv__ = __div__

    def __rdiv__(self, other):
        if isinstance(other, int):
            new_numerator = self.expression.denominator * other
            return rat(new_numerator, self.expression.numerator)
        elif not isinstance(other, rat):
            # do our best type conversion!
            other = rat(other)

        new_num = self.expression.denominator * other.expression.numerator
        new_denom = self.expression.numerator * other.expression.denominator
        return rat(new_num, new_denom)

    __rtruediv__ = __rdiv__

    def __idiv__(self, other):
        # in order to behave like the other numeric types, we make rat immutable, and return a new one in /= cases:
        return self / other

    __itruediv__ = __idiv__
