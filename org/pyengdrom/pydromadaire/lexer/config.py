
import string

NUMBER = "NUMBER"
NAME   = "NAME"

PLUS   = "PLUS"
MINUS  = "MINUS"
TIMES  = "TIMES"
DIVIDE = "DIVIDE"

COMMA = "COMMA"

LBRACKET          = "LBRACKET"
LSQUARED_BRACKET  = "LSQUARED_BRACKET"
LCURLY_BRACKET    = "LCURLY_BRACKET"
RBRACKET          = "RBRACKET"
RSQUARED_BRACKET  = "RSQUARED_BRACKET"
RCURLY_BRACKET    = "RCURLY_BRACKET"

VERT_LINE = "VERT_LINE"

EOF = "EOF"
SET = "SET"

TOKEN_TYPES = [
    NUMBER, NAME, PLUS, MINUS, SET, VERT_LINE, DIVIDE, TIMES,

    LBRACKET        ,
    LSQUARED_BRACKET,
    LCURLY_BRACKET  ,
    RBRACKET        ,
    RSQUARED_BRACKET,
    RCURLY_BRACKET,
    EOF, COMMA
]

START_NAME_STRING = string.ascii_letters + "_"
NAME_STRING = START_NAME_STRING + string.digits

IGNORE_STRING = " \t\r"

from org.pyengdrom.pydromadaire.lexer.operator import Operator

OPERAND_TREE = [
    Operator("+", PLUS,  [
        Operator("=", PLUS + SET, [])
    ]),
    Operator("-", MINUS, [
        Operator("=", MINUS + SET, [])
    ]),
    Operator("*", TIMES,  [
        Operator("=", TIMES + SET, [])
    ]),
    Operator("/", DIVIDE,  [
        Operator("=", DIVIDE + SET, [])
    ]),
    Operator("|", VERT_LINE,  []),
    Operator("[", LSQUARED_BRACKET,  []),
    Operator("]", RSQUARED_BRACKET,  []),
    Operator("(", LBRACKET,  []),
    Operator(")", RBRACKET,  []),
    Operator("{", LCURLY_BRACKET,  []),
    Operator("}", RCURLY_BRACKET,  []),
    Operator("\n", EOF, []),
    Operator(";", EOF, []),
    Operator(",", COMMA, []),
    Operator("=", SET, []),
]