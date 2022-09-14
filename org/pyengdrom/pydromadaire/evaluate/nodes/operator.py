
from org.pyengdrom.pydromadaire.evaluate.nodes.node import EvaluatorNode
from org.pyengdrom.pydromadaire.evaluate.stack import VariableStack

class OperatorNode(EvaluatorNode):
    def __init__(self, left, right, operator):
        self.left  = left
        self.right = right

        self.operator = operator
    def evaluate(self, stack: "VariableStack"):
        return super().evaluate(stack)
    def __str__(self):
        return f"({self.left} {self.operator} {self.right})"
