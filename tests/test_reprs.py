import unittest
from ..eneres_100_hw_libraries.convert import convert
from decimal import Decimal
from unum.units import *


# Some stuff I'd like to represent: 160 billion, 7.05e9, 7.05*10^9, 7.5x10^9, 30%, 346,567,000, 35 MJ / thousand m^3 / 72^2 kg
class ReprTests(unittest.TestCase):
    def test_word(self):
        self.assertEqual(convert("160 billion"), 160e9)

    def test_sci(self):
        self.assertEqual(convert("7.05e9"), Decimal("7.05") * 10**9)

    def test_sci_string(self):
        self.assertEqual(convert("7.05*10^9"), 7.05e9)

    def test_percent(self):
        self.assertEqual(convert("30%"), Decimal("0.3"))

    def test_comma_separated(self):
        self.assertEqual(convert("346,567,000"), 346567000)

    def test_unum(self):
        self.assertEqual(
            convert("35 MJ / thousand m^3 / 72^2 kg"),
            (35 / (1000 * 72**2)) * MJ / (m**3 * kg),
        )

    def test_round(self):
        self.assertAlmostEqual(convert("17.3"), 17.3)

    def test_complex_division(self):
        self.assertEqual(
            convert("2000 * dollar * 0.04/year / 1 - (1 + 0.04)^-20"),
            147.16 * dollar / year,
        )


unittest.main()
