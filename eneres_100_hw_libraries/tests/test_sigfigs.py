# python3 -m eneres_100_hw_libraries.tests.test_sigfigs
import unittest
from ..convert import convert as c
from ..UniversalNumbers import UniversalNumber
from decimal import Decimal
from unum.units import *


class SigFigTests(unittest.TestCase):
    def test_universal(self):
        self.assertIsInstance(c("5"), UniversalNumber)

    def test_simple_int(self):
        num = UniversalNumber.coerce(123000)
        self.assertEqual(num.get_sigfigs(), 3)

    def test_simple_dec(self):
        dec = UniversalNumber.coerce(Decimal("17.400"))
        self.assertEqual(dec.get_sigfigs(), 5)

    def test_str(self):
        rep = UniversalNumber.coerce("0.10")
        self.assertEqual(rep.get_sigfigs(), 2)

    def test_mul(self):
        rep = UniversalNumber.coerce("0.5 x 0.60")
        self.assertEqual(rep.get_sigfigs(), 2)

    def test_word_addition(self):
        rep = UniversalNumber.coerce("10.70 + thousand")
        self.assertEqual(rep.get_sigfigs(), None)

    def test_word_mul(self):
        rep = UniversalNumber.coerce("10.70 * thousand")
        self.assertEqual(rep.get_sigfigs(), 4)

    def test_round(self):
        rep1 = UniversalNumber.coerce("17.6300")
        rep2 = UniversalNumber.coerce("12.7")
        self.assertEqual(round(rep1 * rep2), 224)

    def test_reprs(self):
        rep = UniversalNumber.coerce("120000000.340")
        self.assertEqual(rep.reprs["COMMA"], "120,000,000.340")
        self.assertEqual(str(rep), "1.200000e+08")  # Default


unittest.main()
