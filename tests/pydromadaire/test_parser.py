
from org.pyengdrom.pydromadaire.lexer.config import DIVIDE, MINUS, NAME, NUMBER, PLUS, SET, TIMES
from org.pyengdrom.pydromadaire.lexer.token   import Token
from org.pyengdrom.pydromadaire.parser.config import PyDromConfig
from org.pyengdrom.pydromadaire.parser.cursor import ParserCursor
from org.pyengdrom.pydromadaire.parser.grammar.rulecompiler import RuleCompiler

def test_create_conf():
    PyDromConfig()

def make_sys(tokens, text):
    conf = PyDromConfig()

    cursor = ParserCursor(tokens)
    cursor.set_config(conf)

    rulecompiler = RuleCompiler()
    return conf, cursor, rulecompiler.compile(text, conf)

def test_float():
    tokens = [
        Token((NUMBER, "0123.12")),
        Token((PLUS, "PLUS")),
        Token((NUMBER, "0123"))
    ]
    conf, cursor, rule = make_sys(tokens, "EXPR")
    L = []
    
    rule.link( lambda *a : L.extend(a) )
    rule.parse(cursor)

    assert str(L[0]) == "(123.12 PLUS 123)"
    assert len(L) == 1

def test_token_rule():
    tokens = [
        Token((NAME, "test")),
        Token((NUMBER, "0123"))
    ]
    conf, cursor, rule = make_sys(tokens, "//NAME/ //NUMBER/")
    L = []
    
    rule.link( lambda *a : L.extend(a) )
    rule.parse(cursor)

    assert L[0] == "test"
    assert L[1] == "0123"

def test_many():
    tokens_lists = [
        [
            Token((NAME, "test")),
            Token((NAME, "test")),
            Token((NAME, "test"))
        ],[
            Token((NAME, "test"))
        ], []
    ]
    for tokens in tokens_lists:
        conf, cursor, rule = make_sys(tokens, "//NAME/*")
        L = []
        rule.link( lambda *a : L.extend(a) )
        rule.parse(cursor)

        for i in range(len(tokens)):
            assert L[i] == tokens[i].get_value()

def test_or_rule():
    tokens_lists = [
        [
            Token((NUMBER, "0123"))
        ],[
            Token((NAME, "test"))
        ],[
            Token((PLUS, "plus"))
        ]
    ]
    for tokens in tokens_lists:
        conf, cursor, rule = make_sys(tokens, "//NAME/ | //NUMBER/ | //PLUS/")
        L = []
        rule.link( lambda *a : L.extend(a) )
        rule.parse(cursor)

        for i in range(len(tokens)):
            assert L[i] == tokens[i].get_value()

def test_option_rule():
    tokens_lists = [
        [
            Token((NUMBER, "0123"))
        ], []
    ]
    for tokens in tokens_lists:
        conf, cursor, rule = make_sys(tokens, "[//NUMBER/]")
        L = []
        rule.link( lambda *a : L.extend(a) )
        rule.parse(cursor)

        for i in range(len(tokens)):
            assert L[i] == tokens[i].get_value()

def test_option_and_many():
    tokens_lists = [
        [
            Token((NUMBER, "0124")),
            Token((NUMBER, "0123"))
        ],[
            Token((NUMBER, "0123"))
        ], []
    ]
    for tokens in tokens_lists:
        conf, cursor, rule = make_sys(tokens, "[//NUMBER/]*")
        L = []
        rule.link( lambda *a : L.extend(a) )
        rule.parse(cursor)

        for i in range(len(tokens)):
            assert L[i] == tokens[i].get_value()

def test_list():
    tokens_lists = [
        [
            Token((NUMBER, "0124")),
            Token((NUMBER, "0123")),
            Token((NUMBER, "0123")),
            Token((NAME, "abc"))
        ],[
            Token((NUMBER, "0124")),
            Token((NUMBER, "0123"))
        ],[
            Token((NUMBER, "0124")),
            Token((NUMBER, "0123")),
            Token((NUMBER, "0123")),
            Token((NAME, "abc")),
            Token((NUMBER, "0123")),
            Token((NUMBER, "0123"))
        ]
    ]
    for tokens in tokens_lists:
        conf, cursor, rule = make_sys(tokens, "//NUMBER/ //NUMBER/ [//NUMBER/ | /NAME/]*")
        L = []
        rule.link( lambda *a : L.extend(a) )
        rule.parse(cursor)

        u = 0
        for i in range(len(tokens)):
            if tokens[i].get_type() == NUMBER:
                assert L[u] == tokens[i].get_value()
                u += 1

def test_expr():
    tokens = [
            Token((NUMBER, "0124")),
        ]
    conf, cursor, rule = make_sys(tokens, "EXPR")
    L = []
    rule.link( lambda *a : L.extend(a) )
    rule.parse(cursor)
    assert str(L[0]) == "124"

    tokens = [
            Token((NUMBER, "0124")),
            Token((PLUS, "PLUS")),
            Token((NUMBER, "0123")),
        ]
    conf, cursor, rule = make_sys(tokens, "EXPR")
    L = []
    rule.link( lambda *a : L.extend(a) )
    rule.parse(cursor)
    assert str(L[0]) == "(124 PLUS 123)"
    tokens = [
            Token((NUMBER, "0124")),
            Token((PLUS, "PLUS")),
            Token((NUMBER, "0123")),
            Token((TIMES, "TIMES")),
            Token((NUMBER, "0122")),
        ]
    conf, cursor, rule = make_sys(tokens, "EXPR")
    L = []
    rule.link( lambda *a : L.extend(a) )
    rule.parse(cursor)
    assert str(L[0]) == "(124 PLUS (123 TIMES 122))"

    tokens = [
            Token((NUMBER, "0124")),
            Token((MINUS, "MINUS")),
            Token((NUMBER, "0123")),
            Token((DIVIDE, "DIVIDE")),
            Token((NUMBER, "0122")),
        ]
    conf, cursor, rule = make_sys(tokens, "EXPR")
    L = []
    rule.link( lambda *a : L.extend(a) )
    rule.parse(cursor)
    assert str(L[0]) == "(124 MINUS (123 DIVIDE 122))"

    tokens = [
            Token((NUMBER, "0124")),
            Token((DIVIDE, "DIVIDE")),
            Token((NUMBER, "0123")),
            Token((MINUS, "MINUS")),
            Token((NUMBER, "0122")),
        ]
    conf, cursor, rule = make_sys(tokens, "EXPR")
    L = []
    rule.link( lambda *a : L.extend(a) )
    rule.parse(cursor)
    assert str(L[0]) == "((124 DIVIDE 123) MINUS 122)"

def test_expr_get_node():
    tokens = [
            Token((NAME, "abc")),
            Token((DIVIDE, "DIVIDE")),
            Token((NUMBER, "0123")),
            Token((MINUS, "MINUS")),
            Token((NUMBER, "0122")),
        ]
    conf, cursor, rule = make_sys(tokens, "EXPR")
    L = []
    rule.link( lambda *a : L.extend(a) )
    rule.parse(cursor)
    assert str(L[0]) == "((GET:abc DIVIDE 123) MINUS 122)"

def test_expr_set_node():
    tokens = [
            Token((NAME, "bcd")),
            Token((SET, "SET")),
            Token((NAME, "abc")),
            Token((DIVIDE, "DIVIDE")),
            Token((NUMBER, "0123")),
            Token((MINUS, "MINUS")),
            Token((NUMBER, "0122")),
        ]
    conf, cursor, rule = make_sys(tokens, "EXPR")
    L = []
    rule.link( lambda *a : L.extend(a) )
    rule.parse(cursor)
    assert str(L[0]) == "SET[bcd]:((GET:abc DIVIDE 123) MINUS 122)"
