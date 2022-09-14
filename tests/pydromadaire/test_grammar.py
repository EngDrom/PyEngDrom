
from org.pyengdrom.pydromadaire.evaluate.nodes.grammar.if_node import IfNode
from org.pyengdrom.pydromadaire.evaluate.nodes.block import BlockNode
from org.pyengdrom.pydromadaire.lexer.config import DIVIDE, LBRACKET, LCURLY_BRACKET, MINUS, NAME, NUMBER, PLUS, RBRACKET, RCURLY_BRACKET, SET, TIMES
from org.pyengdrom.pydromadaire.lexer.token   import Token
from org.pyengdrom.pydromadaire.parser.config import PyDromConfig
from org.pyengdrom.pydromadaire.parser.cursor import ParserCursor
from org.pyengdrom.pydromadaire.parser.grammar.rulecompiler import RuleCompiler
from org.pyengdrom.pydromadaire import PyDromLangage

def make_sys(tokens, text):
    conf = PyDromConfig()

    cursor = ParserCursor(tokens)
    cursor.set_config(conf)

    rulecompiler = RuleCompiler()
    return conf, cursor, rulecompiler.compile(text, conf)

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

def test_if_node():
    compiled : BlockNode = PyDromLangage.compile("if (0) {}", "<stdtest>")
    if_node : "IfNode" = compiled.nodes[0]

    assert if_node.else_data == None
    assert len(if_node.else_if_data) == 0
    assert if_node.if_data[0] == 0
    assert isinstance(if_node.if_data[1], BlockNode)
    assert len(if_node.if_data[1].nodes) == 0

    compiled : BlockNode = PyDromLangage.compile("if (0) {a=2}", "<stdtest>")
    if_node : "IfNode" = compiled.nodes[0]

    assert if_node.else_data == None
    assert len(if_node.else_if_data) == 0
    assert if_node.if_data[0] == 0
    assert isinstance(if_node.if_data[1], BlockNode)
    assert len(if_node.if_data[1].nodes) == 1
    assert str(if_node.if_data[1].nodes[0]) == "SET[a]:2"

def test_nested_if_node():
    compiled : BlockNode = PyDromLangage.compile("if (0) {if(1) {a=2}}", "<stdtest>")
    if_node : "IfNode" = compiled.nodes[0]

    assert if_node.else_data == None
    assert len(if_node.else_if_data) == 0
    assert if_node.if_data[0] == 0
    assert isinstance(if_node.if_data[1], BlockNode)
    assert len(if_node.if_data[1].nodes) == 1
    if_node = if_node.if_data[1].nodes[0]

    assert if_node.else_data == None
    assert len(if_node.else_if_data) == 0
    assert if_node.if_data[0] == 1
    assert isinstance(if_node.if_data[1], BlockNode)
    assert len(if_node.if_data[1].nodes) == 1
    assert str(if_node.if_data[1].nodes[0]) == "SET[a]:2"

def test_else_node():
    compiled : BlockNode = PyDromLangage.compile("if (0) {} else {}", "<stdtest>")
    if_node : "IfNode" = compiled.nodes[0]

    assert isinstance(if_node.else_data, BlockNode)
    assert len(if_node.else_data.nodes) == 0
    assert len(if_node.else_if_data) == 0
    assert if_node.if_data[0] == 0
    assert isinstance(if_node.if_data[1], BlockNode)
    assert len(if_node.if_data[1].nodes) == 0

    compiled : BlockNode = PyDromLangage.compile("if (0) {} else {a = 2}", "<stdtest>")
    if_node : "IfNode" = compiled.nodes[0]

    assert isinstance(if_node.else_data, BlockNode)
    assert len(if_node.else_data.nodes) == 1
    assert str(if_node.else_data.nodes[0]) == "SET[a]:2"
    assert len(if_node.else_if_data) == 0
    assert if_node.if_data[0] == 0
    assert isinstance(if_node.if_data[1], BlockNode)
    assert len(if_node.if_data[1].nodes) == 0

def test_else_if_node():
    compiled : BlockNode = PyDromLangage.compile("if (0) {} else if(0) {a = 2} else if (1) {} else {}", "<stdtest>")
    if_node : "IfNode" = compiled.nodes[0]

    assert if_node.if_data[0] == 0
    assert isinstance(if_node.if_data[1], BlockNode)
    assert len(if_node.if_data[1].nodes) == 0

    assert len(if_node.else_if_data) == 4
    assert if_node.else_if_data[0] == 0
    assert isinstance(if_node.else_if_data[1], BlockNode)
    assert len(if_node.else_if_data[1].nodes) == 1
    assert str(if_node.else_if_data[1].nodes[0]) == "SET[a]:2"
    assert if_node.else_if_data[2] == 1
    assert isinstance(if_node.else_if_data[3], BlockNode)
    assert len(if_node.else_if_data[3].nodes) == 0

    assert isinstance(if_node.else_data, BlockNode)
    assert len(if_node.else_data.nodes) == 0
