import unittest
from rat import rat


class RationalsTest(unittest.TestCase):
    def test_creation(self):
        r = rat(22, 7)
        self.assertIsInstance(r, rat)

    def test_rational_addition(self):
        r1 = rat(7, 2)
        r_sum = r1 + r1
        self.assertEqual(r_sum, rat(7))

    def test_rational_subtraction(self):
        r1 = rat(7, 2)
        r_difference = r1 - r1
        self.assertEqual(r_difference, rat(0))

    def test_comparison(self):
        r1 = rat(7, 2)
        r2 = rat(14, 4)
        self.assertEqual(r1, r2)
