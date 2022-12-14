import string
from org.pyengdrom.pydromadaire.lexer.config import EOF, PLUS, SET, MINUS, STRING
from org.pyengdrom.pydromadaire.lexer.lexer import Lexer


def test_single_operand():
    l = Lexer("+", "<stdtest>")
    L = l._build()

    assert len(L) == 2
    assert L[1].get_type() == EOF
    assert L[0].get_type() == PLUS
    assert L[0].size == 1
    assert l.idx == 1


def test_double_operand():
    l = Lexer("+=", "<stdtest>")
    L = l._build()

    assert len(L) == 2
    assert L[0].get_type() == PLUS + SET
    assert L[0].size == 2
    assert l.idx == 2


def test_list_operand():
    l = Lexer("+-+=-=+-++", "<stdtest>")
    L = l._build()

    assert len(L) == 9
    assert L[8].get_type() == EOF
    assert L[0].get_type() == PLUS
    assert L[1].get_type() == MINUS
    assert L[2].get_type() == PLUS + SET
    assert L[3].get_type() == MINUS + SET
    assert L[4].get_type() == PLUS
    assert L[5].get_type() == MINUS
    assert L[6].get_type() == PLUS
    assert L[7].get_type() == PLUS
    assert l.idx == 10


def test_ignorechars():
    l = Lexer(" \n\t\r", "<stdtest>")
    L = l._build()

    assert l.idx == 4
    assert len(L) == 2
    assert L[0].get_type() == EOF
    assert L[1].get_type() == EOF


def test_name():
    l = Lexer(string.ascii_letters, "<stdtest>")
    L = l._build()

    assert l.idx == len(string.ascii_letters)
    assert len(L) == 2

    l = Lexer(string.ascii_letters + "_" + string.digits, "<stdtest>")
    L = l._build()

    assert l.idx == len(string.ascii_letters + "_" + string.digits)
    assert len(L) == 2

    l = Lexer(string.digits + "_" + string.ascii_letters, "<stdtest>")
    L = l._build()

    assert len(L) == 3
    assert l.idx == len(string.ascii_letters + "_" + string.digits)

def test_string():
    l = Lexer("\"abc\\\"\n\''\"", "<stdtest>")
    L = l._build()
    
    assert len(L) == 2
    assert L[0].get_type() == STRING
    assert L[0].get_value() == "abc\"\n\''"
    assert L[1].get_type() == EOF

def test_number():
    l = Lexer(string.digits + " " + string.digits + "." + string.digits, "<stdtest>")
    L = l._build()

    assert len(L) == 3
    assert l.idx == len(l.string)
    assert L[0].get_type() == "NUMBER"
    assert L[1].get_type() == "NUMBER"
    assert L[0].get_value() == string.digits
    assert L[1].get_value() == string.digits + "." + string.digits
    assert L[2].get_type() == EOF
