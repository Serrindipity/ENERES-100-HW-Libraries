from decimal import Decimal, InvalidOperation, getcontext
from unum import Unum
import unum.units as u
import re
import warnings
from typing import Iterable

INSERT_OPERATOR = "*"

verbose = False

# TODO make this return a Universal Number instance


def _simple_process_input(rep: float | int | str | Decimal | Unum) -> Unum:
    """
    Runs a series of quick checks on a given input. Returns a `Unum` if the input is a float, int, etc.
    """

    if isinstance(rep, (float, int)):
        return Unum.coerceToUnum(Decimal(rep))

    if isinstance(rep, (Decimal, Unum)):
        return Unum.coerceToUnum(rep)

    # Handle percents
    if isinstance(rep, str) and rep.endswith("%"):
        try:
            dec = Decimal(rep[:-1]) / 100
        except InvalidOperation:
            raise ValueError(f"Invalid percentage format: {rep}")
        return Unum.coerceToUnum(dec)


def _prep_in_str(in_str: str) -> str:
    out = in_str.strip()
    # Parse comma-separated stuff
    if isinstance(out, str) and "," in out:
        out = out.replace(",", "")
    return out


def _prepare_for_eval(tokens: Iterable) -> str:
    """Prepares `tokens` for evaluation"""

    # Do conversions:
    operators = {"+", "-", "*", "**", "/"}
    opening_separators = {"(", "[", "{"}
    closing_separators = {")", "]", "}"}
    separators = opening_separators | closing_separators

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

        """
        When do we want to insert an operator?
        # 1. Between 2 values
        # 2. Between a closing separator and an opening one without an operator already
        """
        if (
            prev not in operators
            and current not in operators
            and prev not in separators
            and current not in separators
        ):
            final_tokens.append(INSERT_OPERATOR)
        elif prev in closing_separators and current in opening_separators:
            final_tokens.append(INSERT_OPERATOR)

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

    rep = "".join(repr(i) if not isinstance(i, str) else i for i in final_tokens)
    if verbose:
        print(f"Post conversion output is {rep}")
    return rep


allowed_globals = {"__builtins__": None}
allowed_locals = {
    "Decimal": Decimal,
    "e": Decimal("2.718281828459045"),
    "pi": Decimal("3.141592653589793"),
    "math": __import__("math"),  # Import math for math constants if necessary
}
# Add units as allowed_locals
allowed_locals.update({k: v for k, v in vars(u).items() if not k.startswith("_")})

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


def _eval_expr(token_expr: str):
    try:
        # Evaluate the input safely
        evaluated_input = eval(token_expr, allowed_globals, allowed_locals)
        # Convert the result to Decimal
        return (
            evaluated_input
            if isinstance(evaluated_input, Unum)
            else Unum.coerceToUnum(Decimal(evaluated_input))
        )
    except (TypeError, InvalidOperation) as e:
        raise ValueError(f"Invalid number format: {token_expr} \n {e}")


def convert(rep: float | int | str | Decimal | Unum):
    """Returns a Unum object from a variety of number representations. Tokenizes, then parses data, then runs `eval()` on tokens."""
    if isinstance(rep, str):
        rep = _prep_in_str(rep)
    simple = _simple_process_input(rep)
    if simple:
        return simple
    else:
        tokens = tokenize(rep)
        prepared_statement = _prepare_for_eval(tokens)
        return _eval_expr(prepared_statement)


def tokenize(
    expr: str,
    pattern: re.Pattern = r"(-?\d+(?:\.\d+)?(?:e[+\-]?\d+)?|[a-zA-Z]+|\*\*|[+\-*/()^])",
) -> list:
    """Returns tokens for given input. Matches decimals, sci notation, words, operators, separators, ..."""
    tokens = re.findall(pattern, expr, re.VERBOSE)
    return tokens
