
import string

NUMBER = "NUMBER"
NAME   = "NAME"
PLUS   = "PLUS"
MINUS  = "MINUS"
SET    = "SET"

TOKEN_TYPES = [
    NUMBER, NAME, PLUS, MINUS, SET
]

START_NAME_STRING = string.ascii_letters + "_"
NAME_STRING = START_NAME_STRING + string.digits

IGNORE_STRING = " \t\n\r"

from org.pyengdrom.pydromadaire.lexer.operator import Operator

OPERAND_TREE = [
    Operator("+", PLUS,  [
        Operator("=", PLUS + SET, [])
    ]),
    Operator("-", MINUS, [
        Operator("=", MINUS + SET, [])
    ]),
]