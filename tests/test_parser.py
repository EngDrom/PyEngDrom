
from org.pyengdrom.pydromadaire.lexer.config import NAME, NUMBER
from org.pyengdrom.pydromadaire.lexer.token   import Token
from org.pyengdrom.pydromadaire.parser.config import PyDromConfig
from org.pyengdrom.pydromadaire.parser.cursor import ParserCursor
from org.pyengdrom.pydromadaire.parser.grammar.rulecompiler import RuleCompiler

def test_create_conf():
    PyDromConfig()

def test_token():
    conf = PyDromConfig()

    tokens = [
        Token((NAME, "test")),
        Token((NUMBER, "0123"))
    ]

    cursor = ParserCursor(tokens)
    cursor.set_config(conf)

    rulecompiler = RuleCompiler()
    rule = rulecompiler.compile("//NAME/ //NUMBER/", conf).link( print )
    data = rule.parse(cursor)
