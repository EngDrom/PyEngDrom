
from org.pyengdrom.pydromadaire.evaluate.nodes.node import EvaluatorNode
from org.pyengdrom.pydromadaire.evaluate.stack import VariableStack
from org.pyengdrom.pydromadaire.lexer.config import DIVIDE, MINUS, PLUS, TIMES

class OperatorNode(EvaluatorNode):
    def __init__(self, left, right, operator):
        self.left  = left
        self.right = right

        self.operator = operator
    def evaluate(self, stack: "VariableStack"):
        left = self.left
        while isinstance(left, EvaluatorNode): left = left.evaluate(stack)
        right = self.right
        while isinstance(right, EvaluatorNode): right = right.evaluate(stack)

        if self.operator == PLUS  : return left + right
        if self.operator == MINUS : return left - right
        if self.operator == TIMES : return left * right
        if self.operator == DIVIDE: return left / right

        raise Exception(f"Operator {self.operator} could not be found")
    def __str__(self):
        return f"({self.left} {self.operator} {self.right})"
