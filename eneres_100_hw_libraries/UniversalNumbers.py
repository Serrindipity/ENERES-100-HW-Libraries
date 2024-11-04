# Universal Numbers

# Some stuff I'd like to represent: 160 billion, 7.05e9, 7.05*10^9, 7.5x10^9, 30%, 346,567,000

from decimal import Decimal, InvalidOperation, getcontext
from unum import Unum
import unum.units as u
import re
import warnings
from typing import Iterable
from eneres_100_hw_libraries.convert import convert, tokenize


# TODO: Look at splitting parse input type functionality into multiple functions to reuse for this method
def find_sigfigs(rep: float | int | str | Decimal | Unum) -> int:
    """Returns the number of significant figures for the given input."""
    try:
        return _sigfig(rep)
    except:
        tokens = tokenize(rep)
        if len(tokens) == 1:
            return _sigfig(tokens[0])
        else:
            raise NotImplementedError


def _sigfig(rep: float | int | str | Decimal | Unum) -> int:
    """
    Returns the number of significant figures for a singular input. May be `Decimal('Infinity')` if the figure is exact. Should *only* be called on input for a single token. Maybe return 0 if token should be ignored?
    >>> _sigfig(123000)
    3
    >>> _sigfig(Decimal('1600.026'))
    7
    """

    FLOAT_ZEROS_THRESHOLD = 5

    inf = {
        "hundred",
        "thousand",
        "million",
        "billion",
        "trillion",
        "quadrillion",
        "quintillion",
        "sextillion",
    }
    if isinstance(rep, int):
        # This is a bit hacky, but it works? Might want to look for a more elegant way to do this.
        return len(str(rep).rstrip("0"))

    if isinstance(rep, Decimal):
        str_repr = str(rep)
        parts = str_repr.split(".")
        if len(parts) == 1:
            return _sigfig(
                int(parts[0])
            )  # Turns it into an int and runs it back into _sigfig
        else:
            assert len(parts) == 2
            figs = 0
            # Currently adds the length of the first part, then the length of the second part minus the decimal point. This could *definitely* be simplified.
            figs += len(parts[0]) if int(parts[0]) != 0 else 0
            figs += len(parts[1].removeprefix("."))
            return figs

    if isinstance(rep, Unum):
        return _sigfig(rep.asNumber())

    if isinstance(rep, float):
        warnings.warn(
            "Float passed to sigfig check... Did you mean to pass in a Decimal?",
            SyntaxWarning,
        )
        # Just coerces it back to a decimal and passes it back to the function lol
        return _sigfig(Decimal(rep))
    if isinstance(rep, str) and rep in inf:
        return Decimal("Infinity")
    try:
        return _sigfig(Decimal(rep))
    except:
        raise InvalidOperation("Sigfigs could not be extracted from token")


# TODO: Refactor this so that all internal methods get overriden by the unum inside it
# TODO: Make all reprs print the unum
class UniversalNumber:

    REPR_TYPES = {"COMMA", "SCI", "DEFAULT", "DECIMAL"}

    def __init__(self, unum, sfs) -> None:
        self.unum: Unum = unum
        self.sigfigs: int = sfs
        self.reprs: dict = self.generate_reprs()

        # Grabs all the methods of Unum and set them as attributes of UniversalNumber. This is **so bad** and I should prob just use inheritance instead.
        # ignore = {"__init__", "__class__"}
        # method_list = [
        #     func
        #     for func in dir(Unum)
        #     if (callable(getattr(Unum, func)) and func not in ignore)
        # ]
        # for f in method_list:
        #     func = getattr(Unum, f)
        #     overloaded_f = lambda self, *otherargs: self.unum.func(*otherargs)
        #     setattr(self, f, overloaded_f)

    def coerce(rep, sigfigs: int = None):
        """Returns a UniversalNumber with sigfigs and unum from the given input. Attempts to calculate the number of sigfigs if not passed in."""
        if isinstance(rep, UniversalNumber):
            return rep
        unum: Unum = convert(rep)
        sf: int = sigfigs if sigfigs else find_sigfigs(rep)
        return UniversalNumber(unum, sf)

    coerce = staticmethod(coerce)

    __slots__ = ("unum", "sigfigs", "reprs", "__dict__")

    # Operations
    # TODO: Add and sub should work based on decimal places, not sigfigs
    def __add__(self, other):
        pass

    def __sub__(self, other):
        pass

    def __mul__(self, other):
        o = UniversalNumber.coerce(other)
        return UniversalNumber(
            self.unum * other, min(self.get_sigfigs(), o.get_sigfigs())
        )

    def __truediv__(self, other):
        o = UniversalNumber.coerce(other)
        return UniversalNumber(
            self.unum / other, min(self.get_sigfigs(), o.get_sigfigs())
        )

    def __eq__(self, other: object) -> bool:
        return round(self) == round(other)

    # Others
    def __str__(self):
        if not self.unum // 1000000:
            return self.reprs["COMMA"]
        else:
            return self.reprs["DEFAULT"]

    def __repr__(self):
        return f"UniversalNumber({self.reprs['DEFAULT']})"

    def __round__(self):
        return UniversalNumber(round(self.unum, self.sigfigs), self.sigfigs)

    def get_sigfigs(self) -> int:
        return self.sigfigs

    # TODO change this to represent sigfigs also?
    def generate_reprs(self) -> dict:
        """Returns a `dict` of number representations. Should return **COMMA**, **SCI**, and **DEFAULT** reprs at least."""
        reprs = {"DEFAULT": str(self.unum)}
        unit_str = self.unum.strUnit()
        if unit_str:
            unit_str = Unum.UNIT_INDENT + unit_str

        decimal_repr = (str(Decimal(self.unum.asNumber())) + unit_str).strip()
        reprs["DECIMAL"] = decimal_repr

        comma_repr = f"{self.unum.asNumber():,}{unit_str}"
        reprs["COMMA"] = comma_repr

        return reprs

    def get_reprs(self) -> dict:
        return self.reprs


if __name__ == "__main__":
    import doctest

    doctest.testmod()
