
import string

NUMBER = "NUMBER"
NAME   = "NAME"
STRING = "STRING"

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

EQUALS = "EQUALS"
GREATER = "GREATER"
LESS = "LESS"
NOT = "NOT"
OR = "OR"
XOR = "XOR"
AND = "AND"
B_OR = VERT_LINE
B_AND = "B_AND"
DOT = "DOT"

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
    Operator("|", VERT_LINE,  [  # B_OR
        Operator("|", OR, [])
    ]),
    Operator("[", LSQUARED_BRACKET,  []),
    Operator("]", RSQUARED_BRACKET,  []),
    Operator("(", LBRACKET,  []),
    Operator(")", RBRACKET,  []),
    Operator("{", LCURLY_BRACKET,  []),
    Operator("}", RCURLY_BRACKET,  []),
    Operator("\n", EOF, []),
    Operator(";", EOF, []),
    Operator(",", COMMA, []),
    Operator("=", SET, [
        Operator("=", EQUALS, [])
    ]),
    Operator("<", LESS, [
        Operator("=", LESS + EQUALS, [])
    ]),
    Operator(">", GREATER, [
        Operator("=", GREATER + EQUALS, [])
    ]),
    Operator("!", NOT, [
        Operator("=", NOT + EQUALS, [])
    ]), 
    Operator("&", B_AND, [
        Operator("&", AND, [])
    ]), 
    Operator("^", XOR, []),
    Operator(".", DOT, [])
]

ESCAPE_CHARS_EQUIVALENT = ["\\a", "\\b", "\\f", "\\n", "\\r", "\\t", "\\v", "\\'", "\\\"", "\\\\"]
ESCAPE_CHARS = ["\a", "\b", "\f", "\n", "\r", "\t", "\v", "\'", "\"", "\\"]