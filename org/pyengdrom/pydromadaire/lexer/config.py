
import string
from org.pyengdrom.pydromadaire.lexer.operator import Operator

NUMBER = "NUMBER"
NAME   = "NAME"
PLUS   = "PLUS"
MINUS  = "MINUS"
SET    = "SET"

TOKEN_TYPES = [
    NUMBER, NAME, PLUS, MINUS, SET
]

OPERAND_TREE = [
    Operator("+", PLUS,  [
        Operator("=", PLUS + SET, [])
    ]),
    Operator("-", MINUS, [
        Operator("=", MINUS + SET, [])
    ]),
]

START_NAME_STRING = string.ascii_letters + "_"
NAME_STRING = START_NAME_STRING + string.digits

IGNORE_STRING = " \t\n\r"
