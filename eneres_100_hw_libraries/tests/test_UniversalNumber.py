# python3 -m eneres_100_hw_libraries.tests.test_UniversalNumber
import unittest
from ..convert import convert as c
from ..UniversalNumbers import UniversalNumber
from decimal import Decimal
from unum.units import *


class SigFigTests(unittest.TestCase):
    def test_universal(self):
        self.assertIsInstance(c("5"), UniversalNumber)

    def test_dot(self):
        s = UniversalNumber.coerce("130.")
        self.assertEqual(s.get_sigfigs(), 3)

    def test_add(self):
        s = UniversalNumber.coerce("17.3")
        o = UniversalNumber.coerce("3.5")
        self.assertEqual(s + o, Decimal("20.8"))

    def test_sub(self):
        s = UniversalNumber.coerce("170.52")
        o = UniversalNumber.coerce("20.7")
        self.assertEqual(s - o, Decimal("150.45"))

    def test_mul(self):
        s = UniversalNumber.coerce("1.4")
        pass


unittest.main()
