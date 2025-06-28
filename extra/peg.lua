import ppeg

digit = RANGE("0-9")
alpha = RANGE("a-z", "A-Z")
alphanum = alpha / num

number = digit?
ident = alpha + alphanum*

addop = SET("+-")
mulop = SET("*/")

grammar = PATTERN(
    factor = number / "(" + expr + ")" / ident,
    term = CAPTURE(factor + (mulop + factor)*) -> AddBinOp,
    expr = CAPTURE(term + (addop + term)*) -> AddBinOp,
)

grammar.start(expr)

grammar.match("2+(3*5-4)-4*2")
