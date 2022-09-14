
from org.pyengdrom.pydromadaire.evaluate.nodes.block import BlockNode
from org.pyengdrom.pydromadaire.evaluate.stack import VariableStack
from org.pyengdrom.pydromadaire import PyDromLangage

def make_evaluation(text):
    nodes : BlockNode = PyDromLangage.compile(text, "<stdtest>")
    stack = VariableStack(None)
    nodes.evaluate(stack)

    return stack

def test_set():
    stack = make_evaluation("a=1")

    assert stack["a"] == 1
    assert len(stack.dict.keys()) == 1
def test_get():
    stack = make_evaluation("a=1;b=a")

    assert stack["a"] == 1
    assert stack["b"] == 1
    assert len(stack.dict.keys()) == 2

def test_operator():
    stack = make_evaluation("a=1+1;b=1-1;c=1*1;d=1/1;e=1*2+1/3-1*5-1/6")

    assert stack["a"] == 2
    assert stack["b"] == 0
    assert stack["c"] == 1
    assert stack["d"] == 1
    assert abs(stack["e"] - (-3 + 1/6)) <= 10 ** -6
    assert len(stack.dict.keys()) == 5

def test_if():
    stack = make_evaluation("if (1) {b = 1}; if(0) {a = 2}")
    assert len(stack.dict.keys()) == 1
    assert stack["b"] == 1

    stack = make_evaluation("if(0) {b = 2} else {a = 1}")
    assert len(stack.dict.keys()) == 1
    assert stack["a"] == 1
    stack = make_evaluation("if(1) {b = 2} else {a = 1}")
    assert len(stack.dict.keys()) == 1
    assert stack["b"] == 2

    stack = make_evaluation("if(0) {b = 2} else if(0) {c = 3} else {a = 1}")
    assert len(stack.dict.keys()) == 1
    assert stack["a"] == 1
    stack = make_evaluation("if(0) {b = 2} else if(1) {c = 3} else {a = 1}")
    assert len(stack.dict.keys()) == 1
    assert stack["c"] == 3
    stack = make_evaluation("if(1) {b = 2} else if(1) {c = 3} else {a = 1}")
    assert len(stack.dict.keys()) == 1
    assert stack["b"] == 2
    stack = make_evaluation("if(1) {b = 2} else if(0) {c = 3} else {a = 1}")
    assert len(stack.dict.keys()) == 1
    assert stack["b"] == 2

    stack = make_evaluation("if(0) {b = 2} else if(0) {c = 3} else if(0) {d = 4} else {a = 1}")
    assert len(stack.dict.keys()) == 1
    assert stack["a"] == 1
    stack = make_evaluation("if(0) {b = 2} else if(1) {c = 3} else if(0) {d = 4} else {a = 1}")
    assert len(stack.dict.keys()) == 1
    assert stack["c"] == 3
    stack = make_evaluation("if(1) {b = 2} else if(1) {c = 3} else if(0) {d = 4} else {a = 1}")
    assert len(stack.dict.keys()) == 1
    assert stack["b"] == 2
    stack = make_evaluation("if(1) {b = 2} else if(0) {c = 3} else if(0) {d = 4} else {a = 1}")
    assert len(stack.dict.keys()) == 1
    assert stack["b"] == 2
    stack = make_evaluation("if(0) {b = 2} else if(0) {c = 3} else if(1) {d = 4} else {a = 1}")
    assert len(stack.dict.keys()) == 1
    assert stack["d"] == 4
    stack = make_evaluation("if(0) {b = 2} else if(1) {c = 3} else if(1) {d = 4} else {a = 1}")
    assert len(stack.dict.keys()) == 1
    assert stack["c"] == 3
    stack = make_evaluation("if(1) {b = 2} else if(1) {c = 3} else if(1) {d = 4} else {a = 1}")
    assert len(stack.dict.keys()) == 1
    assert stack["b"] == 2
    stack = make_evaluation("if(1) {b = 2} else if(0) {c = 3} else if(1) {d = 4} else {a = 1}")
    assert len(stack.dict.keys()) == 1
    assert stack["b"] == 2

def test_while_node():
    stack = make_evaluation("a = 0; while (a) {b = 0}")
    assert len(stack.dict.keys()) == 1
    assert stack["a"] == 0

    stack = make_evaluation("a = 1; while (a) {b = 0; a = 0}")
    assert len(stack.dict.keys()) == 2
    assert stack["a"] == 0
    assert stack["b"] == 0

    stack = make_evaluation("a = 2; b = 1; while (a) {b = b + 1; a = a - 1}")
    assert len(stack.dict.keys()) == 2
    assert stack["a"] == 0
    assert stack["b"] == 3

def test_array_construction():
    stack = make_evaluation("b = 2; a = [1, b + 2]")
    assert len(stack.dict.keys()) == 2
    assert stack["a"] == [1, 4]
    assert stack["b"] == 2