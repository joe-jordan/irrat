from __future__ import division
import unittest
from irrat.rat import rat


class RatArithmeticTests(unittest.TestCase):
    def test_addition_of_integers(self):
        five = rat(5)
        six = five + rat(1)
        self.assertEqual(six.expression.numerator, 6)
        self.assertEqual(six.expression.denominator, 1)

        six = five + 1
        self.assertEqual(six.expression.numerator, 6)
        self.assertEqual(six.expression.denominator, 1)

        six = rat(1) + five
        self.assertEqual(six.expression.numerator, 6)
        self.assertEqual(six.expression.denominator, 1)

        six = 1 + five
        self.assertEqual(six.expression.numerator, 6)
        self.assertEqual(six.expression.denominator, 1)

    def test_addition_of_fractions(self):
        two_thirds = rat(2, 3)
        one = two_thirds + rat(1, 3)
        self.assertEqual(one.expression.numerator, 1)
        self.assertEqual(one.expression.denominator, 1)

        four_thirds = two_thirds + rat(2, 3)
        self.assertEqual(four_thirds.expression.numerator, 4)
        self.assertEqual(four_thirds.expression.denominator, 3)

    def test_immutability_under_addition(self):
        five = rat(5)
        copy_of_five = five
        five += rat(0)
        self.assertEqual(five.expression.numerator, copy_of_five.expression.numerator)
        self.assertEqual(five.expression.denominator, copy_of_five.expression.denominator)
        self.assertIsNot(five, copy_of_five)

        five += 8
        self.assertEqual(copy_of_five.expression.numerator, 5)
        self.assertEqual(copy_of_five.expression.denominator, 1)

        self.assertEqual(five.expression.numerator, 13)
        self.assertEqual(five.expression.denominator, 1)

    def test_subtraction_of_integers(self):
        five = rat(5)
        four = five - rat(1)
        self.assertEqual(four.expression.numerator, 4)
        self.assertEqual(four.expression.denominator, 1)

        four = five - 1
        self.assertEqual(four.expression.numerator, 4)
        self.assertEqual(four.expression.denominator, 1)

        four = rat(1) - five
        self.assertEqual(four.expression.numerator, -4)
        self.assertEqual(four.expression.denominator, 1)

        four = 1 - five
        self.assertEqual(four.expression.numerator, -4)
        self.assertEqual(four.expression.denominator, 1)

    def test_subtraction_of_fractions(self):
        seven_thirds = rat(7, 3)
        one = seven_thirds - rat(4, 3)
        self.assertEqual(one.expression.numerator, 1)
        self.assertEqual(one.expression.denominator, 1)

        four_thirds = seven_thirds - 1
        self.assertEqual(four_thirds.expression.numerator, 4)
        self.assertEqual(four_thirds.expression.denominator, 3)

    def test_immutability_under_subtraction(self):
        five = rat(5)
        copy_of_five = five
        five -= rat(0)
        self.assertEqual(five.expression.numerator, copy_of_five.expression.numerator)
        self.assertEqual(five.expression.denominator, copy_of_five.expression.denominator)
        self.assertIsNot(five, copy_of_five)

        five -= 8
        self.assertEqual(copy_of_five.expression.numerator, 5)
        self.assertEqual(copy_of_five.expression.denominator, 1)

        self.assertEqual(five.expression.numerator, -3)
        self.assertEqual(five.expression.denominator, 1)

    def test_multiplication_of_integers(self):
        five = rat(5)
        ten = five * rat(2)
        self.assertEqual(ten.expression.numerator, 10)
        self.assertEqual(ten.expression.denominator, 1)

        ten = five * 2
        self.assertEqual(ten.expression.numerator, 10)
        self.assertEqual(ten.expression.denominator, 1)

        ten = rat(2) * five
        self.assertEqual(ten.expression.numerator, 10)
        self.assertEqual(ten.expression.denominator, 1)

        ten = 2 * five
        self.assertEqual(ten.expression.numerator, 10)
        self.assertEqual(ten.expression.denominator, 1)

    def test_multiplication_of_fractions(self):
        seven_thirds = rat(7, 3)
        one = seven_thirds * rat(3, 7)
        self.assertEqual(one.expression.numerator, 1)
        self.assertEqual(one.expression.denominator, 1)

        seven = seven_thirds * rat(3)
        self.assertEqual(seven.expression.numerator, 7)
        self.assertEqual(seven.expression.denominator, 1)

        eleven_thirds = seven_thirds * rat(11, 7)
        self.assertEqual(eleven_thirds.expression.numerator, 11)
        self.assertEqual(eleven_thirds.expression.denominator, 3)

    def test_immutability_under_multiplication(self):
        five = rat(5)
        copy_of_five = five
        five *= rat(1)
        self.assertEqual(five.expression.numerator, copy_of_five.expression.numerator)
        self.assertEqual(five.expression.denominator, copy_of_five.expression.denominator)
        self.assertIsNot(five, copy_of_five)

        five *= rat(-2, 7)
        self.assertEqual(copy_of_five.expression.numerator, 5)
        self.assertEqual(copy_of_five.expression.denominator, 1)

        self.assertEqual(five.expression.numerator, -10)
        self.assertEqual(five.expression.denominator, 7)

    def test_division_of_integers(self):
        five = rat(5)
        ten = five / rat(2)
        self.assertEqual(ten.expression.numerator, 5)
        self.assertEqual(ten.expression.denominator, 2)

        ten = five / 2
        self.assertEqual(ten.expression.numerator, 5)
        self.assertEqual(ten.expression.denominator, 2)

        ten = rat(2) / five
        self.assertEqual(ten.expression.numerator, 2)
        self.assertEqual(ten.expression.denominator, 5)

        ten = 2 / five
        self.assertEqual(ten.expression.numerator, 2)
        self.assertEqual(ten.expression.denominator, 5)

    def test_division_of_fractions(self):
        seven_thirds = rat(7, 3)
        one = seven_thirds / rat(7, 3)
        self.assertEqual(one.expression.numerator, 1)
        self.assertEqual(one.expression.denominator, 1)

        one_third = seven_thirds / rat(7)
        self.assertEqual(one_third.expression.numerator, 1)
        self.assertEqual(one_third.expression.denominator, 3)

        forty_nine_thirty_thirds = seven_thirds / rat(11, 7)
        self.assertEqual(forty_nine_thirty_thirds.expression.numerator, 49)
        self.assertEqual(forty_nine_thirty_thirds.expression.denominator, 33)

    def test_floor_division_of_fractions(self):
        seven_thirds = rat(7, 3)
        one = seven_thirds // rat(7, 3)
        self.assertEqual(one.expression.numerator, 1)
        self.assertEqual(one.expression.denominator, 1)

        zero = seven_thirds // rat(7)
        self.assertEqual(zero.expression.numerator, 0)
        self.assertEqual(zero.expression.denominator, 1)

        one = seven_thirds // rat(11, 7)
        self.assertEqual(one.expression.numerator, 1)
        self.assertEqual(one.expression.denominator, 1)

    def test_immutability_under_division(self):
        five = rat(5)
        copy_of_five = five
        five /= rat(1)
        self.assertEqual(five.expression.numerator, copy_of_five.expression.numerator)
        self.assertEqual(five.expression.denominator, copy_of_five.expression.denominator)
        self.assertIsNot(five, copy_of_five)

        five /= rat(-2, 7)
        self.assertEqual(copy_of_five.expression.numerator, 5)
        self.assertEqual(copy_of_five.expression.denominator, 1)

        self.assertEqual(five.expression.numerator, -35)
        self.assertEqual(five.expression.denominator, 2)


class RatUsageTests(unittest.TestCase):
    def test_accuracy_after_float_conversion(self):
        # This test was initially hilariously slow. We added the cautious factorize & prime gen
        # and made it workable.
        r = rat(23, 169)
        s = str(r)
        f = float(s)
        self.assertLess(abs(f - r), 0.001)

    def test_comparison_operators(self):
        ten = rat(10)
        three_halves = rat(3, 2)
        one_tenth = rat(1, 10)
        ten_percent = rat(100, 1000)

        self.assertGreater(ten, three_halves)
        self.assertLessEqual(three_halves, ten)
        self.assertLess(1, three_halves)
        self.assertGreater(ten, 9.9993)
        self.assertLess(one_tenth, three_halves)
        self.assertGreaterEqual(one_tenth, ten_percent)
        self.assertEqual(one_tenth, ten_percent)
        self.assertEqual(one_tenth, 0.1)
