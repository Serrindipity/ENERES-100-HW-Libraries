# Universal Numbers

# Some stuff I'd like to represent: 160 billion, 7.05e9, 7.05*10^9, 7.5x10^9, 30%, 346,567,000

from decimal import Decimal, InvalidOperation, getcontext
from unum import Unum
import unum.units as u
import re


verbose = False
"""
Returns a Unum object from a variety of number representations. Parses data, then tokenizes, then runs eval() on tokens
"""


def _parse_input_type(input: float | int | str | Decimal | Unum) -> Unum:
    getcontext().prec = 7

    if isinstance(input, (float, int)):
        return Unum.coerceToUnum(Decimal(input))

    if isinstance(input, (Decimal, Unum)):
        return Unum.coerceToUnum(input)

    # Parse comma-separated stuff
    if isinstance(input, str) and "," in input:
        input = input.replace(",", "")

    # Handle percents
    if isinstance(input, str) and input.endswith("%"):
        try:
            dec = Decimal(input[:-1]) / 100
        except InvalidOperation:
            raise ValueError(f"Invalid percentage format: {input}")
        return Unum.coerceToUnum(dec)
    # Do conversions:

    conversions = {
        "hundred": Decimal(10**2),
        "thousand": Decimal(10**3),
        "million": Decimal(10**6),
        "billion": Decimal(10**9),
        "trillion": Decimal(10**12),
        "quadrillion": Decimal(10**15),
        "quintillion": Decimal(10**18),
        "sextillion": Decimal(10**21),
        "per": "/",
        "x": "*",
        "^": "**",
    }
    operators = ["+", "-", "*", "**", "/"]

    in_str = input.strip()
    tokens = tokenize(in_str, None)
    if verbose:
        print(tokens)
    converted_tokens = []
    for i in tokens:
        if i in conversions.keys():
            converted_tokens.append(conversions[i])
        else:
            try:
                if verbose:
                    print(i)
                converted_tokens.append(Decimal(i))
            except (InvalidOperation, TypeError):
                converted_tokens.append(i)
                # print("Decimal coercion failed")
    if verbose:
        print(f"converted tokens = {converted_tokens}")
    final_tokens = []

    # Add INSERT_OPERATOR between all tokens without operators between them
    for prev, current in zip(converted_tokens, converted_tokens[1:]):
        final_tokens.append(prev)
        if prev not in operators and current not in operators:
            final_tokens.append(UniversalNumber.INSERT_OPERATOR)
    final_tokens.append(converted_tokens[-1])

    # Add parentheses after /
    i = 0
    while i < len(final_tokens):
        if final_tokens[i] == "/":
            final_tokens.insert(i + 1, "(")
            j = i + 2
            search = True
            while search:
                j += 1
                if j == len(final_tokens):
                    final_tokens.append(")")
                    search = False
                    i = j
                elif final_tokens[j] == "/":
                    final_tokens.insert(j, ")")
                    search = False
                    i = j  # i will automatically increment
        i += 1

    input = "".join(repr(i) if not isinstance(i, str) else i for i in final_tokens)
    if verbose:
        print(f"Post conversion output is {input}")

    # Allow only safe operations and scientific notation and Unum units
    allowed_globals = {"__builtins__": None}
    allowed_locals = {
        "Decimal": Decimal,
        "e": Decimal("2.718281828459045"),
        "pi": Decimal("3.141592653589793"),
        "math": __import__("math"),  # Import math for math constants if necessary
    }
    # Add units as allowed_locals
    allowed_locals.update({k: v for k, v in vars(u).items() if not k.startswith("_")})
    try:

        # Evaluate the input safely
        evaluated_input = eval(input, allowed_globals, allowed_locals)

        # Convert the result to Decimal
        return (
            evaluated_input
            if isinstance(evaluated_input, Unum)
            else Unum.coerceToUnum(Decimal(evaluated_input))
        )
    except (TypeError, InvalidOperation):
        raise ValueError(f"Invalid number format: {input}")


class UniversalNumber:
    INSERT_OPERATOR = "*"

    def __init__(self, input) -> None:
        self.dec = _parse_input_type(input)
        self.reprs = self.generate_reprs()

    # Operations
    def __add__(self, other):
        if isinstance(other, UniversalNumber):
            return UniversalNumber(self.dec + other.dec)
        return UniversalNumber(self.dec + Decimal(other))

    def __sub__(self, other):
        if isinstance(other, UniversalNumber):
            return UniversalNumber(self.dec - other.dec)
        return UniversalNumber(self.dec - Decimal(other))

    def __mul__(self, other):
        if isinstance(other, UniversalNumber):
            return UniversalNumber(self.dec * other.dec)
        return UniversalNumber(self.dec * Decimal(other))

    def __truediv__(self, other):
        if isinstance(other, UniversalNumber):
            return UniversalNumber(self.dec / other.dec)
        return UniversalNumber(self.dec / Decimal(other))

    def __str__(self):
        if not self.dec // 1000000:
            return self.reprs["comma"]
        else:
            return self.reprs["sci"]

    def __repr__(self):
        return f"UniversalNumber({self.reprs['dec']})"

    def generate_reprs(self) -> dict:
        comma_repr = f"{self.dec:,}"
        sci_repr = "%e" % self.dec
        return {"dec": self.dec, "comma": comma_repr, "sci": sci_repr}


def tokenize(expr: str, pattern: re.Pattern | None) -> list:
    token_pattern = (
        r"(\d+(?:\.\d+)?(?:e[+\-]?\d+)?|[a-zA-Z]+|\*\*|[+\-*/()^])"
        if not pattern
        else pattern
    )
    tokens = re.findall(token_pattern, expr, re.VERBOSE)
    return tokens
