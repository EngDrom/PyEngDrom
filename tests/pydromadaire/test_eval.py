
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