
from org.pyengdrom.pydromadaire.evaluate.nodes.block import BlockNode
from org.pyengdrom.pydromadaire.evaluate.stack import VariableStack
from org.pyengdrom.pydromadaire import PyDromLangage

def make_evaluation(text, __global__=None):
    nodes : BlockNode = PyDromLangage.compile(text, "<stdtest>")
    stack = VariableStack(__global__)
    nodes.evaluate(stack)

    return stack

def test_set():
    stack = make_evaluation("a=1")

    assert stack["a"] == 1
    assert len(stack.dict.keys()) == 1
def test_set_at():
    stack = make_evaluation("a=[1, 2]; a[0] = 2; a[1] = 1")

    assert len(stack.dict.keys()) == 1
    assert stack["a"] == [2, 1]
def test_nested_set_at():
    stack = make_evaluation("a=[[[1], [2]], [[3], [4]]]; a[0][0][0] = 4; a[0][1][0] = 3; a[1][0][0] = 2; a[1][1][0] = 1")

    assert len(stack.dict.keys()) == 1
    assert stack["a"] == [[[4], [3]], [[2], [1]]]
def test_get():
    stack = make_evaluation("a=1;b=a")

    assert stack["a"] == 1
    assert stack["b"] == 1
    assert len(stack.dict.keys()) == 2
def test_get_at():
    stack = make_evaluation("a=[1, 2]; b = a[0]; c=a[1]")
    assert len(stack.dict.keys()) == 3
    assert stack["a"] == [1, 2]
    assert stack["b"] == 1
    assert stack["c"] == 2
def test_call():
    L = []
    stack = VariableStack(None)
    stack.__setitem__("func", lambda *a: L.append(a))

    stack = make_evaluation("a=1; func(a, a+1, 2)", stack)
    
    assert L == [(1, 2, 2)]
def test_nested_call():
    L = []
    stack = VariableStack()
    F = lambda *a: (L.append(a), F)[1]
    stack.__setitem__("func", F)

    stack = make_evaluation("a=1; func(a, a+1, 2)(a, a+2, 3)", stack)
    
    assert L == [(1, 2, 2), (1, 3, 3)]
def test_array_call():
    L = []
    stack = VariableStack()
    F = lambda *a: (L.append(a), [F])[1]
    stack.__setitem__("func", [0, F])

    stack = make_evaluation("a=1; func[1](a, a+1, 2)[0](a, a+2, 3)", stack)
    
    assert L == [(1, 2, 2), (1, 3, 3)]

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


def test_function_node():
    stack = make_evaluation("function f() {\na = 0;\n}; f()")
    assert len(stack.dict.keys()) == 1
    assert "f" in stack.dict.keys()

    stack = make_evaluation("function f(L, a) {L[0] = a}; a = [0]; f(a, 1)")
    assert len(stack.dict.keys()) == 2
    assert "f" in stack.dict.keys()
    assert stack["a"] == [1]