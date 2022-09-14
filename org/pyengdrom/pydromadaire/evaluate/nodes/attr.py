

from org.pyengdrom.pydromadaire.evaluate.nodes.node import EvaluatorNode
from org.pyengdrom.pydromadaire.evaluate.stack import VariableStack


class GetNode(EvaluatorNode):
    def __init__(self, name):
        self.name = name
    def evaluate(self, stack: "VariableStack"):
        return stack[self.name]
    def __str__(self):
        return f"GET:{self.name}"

class SetNode(EvaluatorNode):
    def __init__(self, name, expr):
        self.name = name
        self.expr = expr
    def evaluate(self, stack: "VariableStack"):
        value = self.expr
        while isinstance(value, EvaluatorNode): value = value.evaluate(stack)
        
        stack[self.name] = self.expr
        return value
    def __str__(self):
        return f"SET[{self.name}]:{self.expr}"
