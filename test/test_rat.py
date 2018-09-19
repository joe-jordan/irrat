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

