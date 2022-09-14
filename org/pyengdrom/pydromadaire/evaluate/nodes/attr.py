

from org.pyengdrom.pydromadaire.evaluate.nodes.node import EvaluatorNode
from org.pyengdrom.pydromadaire.evaluate.stack import VariableStack


class GetNode(EvaluatorNode):
    def __init__(self, name):
        self.name = name
    def evaluate(self, stack: "VariableStack"):
        return stack[self.name]
    def __str__(self):
        return f"GET:{self.name}"
    def set(self, stack: "VariableStack", value):
        stack[self.name] = value

class GetAtNode(EvaluatorNode):
    def __init__(self, left, expr):
        self.left = left
        self.expr = expr
    def evaluate(self, stack: "VariableStack"):
        left = self.eval(self.left, stack)
        expr = self.eval(self.expr, stack)

        return left[expr]
    def __str__(self):
        return f"{self.left}.AT({self.expr})"
    def set(self, stack: "VariableStack", value):
        left = self.eval(self.left, stack)
        expr = self.eval(self.expr, stack)

        left[expr] = value
        return value
        

class SetNode(EvaluatorNode):
    def __init__(self, name, expr):
        self.name = name
        self.expr = expr
    def evaluate(self, stack: "VariableStack"):
        value = self.expr
        while isinstance(value, EvaluatorNode): value = value.evaluate(stack)
        
        self.name.set(stack, value)
        return value
    def __str__(self):
        return f"SET[{self.name}]:{self.expr}"
