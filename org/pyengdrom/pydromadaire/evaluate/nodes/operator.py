
from org.pyengdrom.pydromadaire.evaluate.nodes.node import EvaluatorNode
from org.pyengdrom.pydromadaire.evaluate.stack import VariableStack
from org.pyengdrom.pydromadaire.lexer.config import AND, B_AND, B_OR, DIVIDE, EQUALS, GREATER, LESS, MINUS, NOT, OR, PLUS, TIMES, XOR

class UnaryNode(EvaluatorNode):
    def __init__(self, left, operator):
        self.left = left
        self.operator = operator
    def evaluate(self, stack: "VariableStack"):
        left = self.eval(self.left, stack)

        if self.operator == NOT: return not left
        if self.operator == MINUS: return - left

        raise Exception(f"Operator {self.operator} could not be found")

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
        
        if self.operator == XOR  : return left ^ right
        if self.operator == B_OR : return left | right
        if self.operator == B_AND: return left & right
        if self.operator == OR: return left or right
        if self.operator == AND: return left and right

        if self.operator == GREATER: return left > right
        if self.operator == GREATER + EQUALS: return left >= right
        if self.operator == LESS: return left < right
        if self.operator == LESS + EQUALS: return left <= right
        if self.operator == EQUALS: return left == right
        if self.operator == NOT + EQUALS: return left != right

        raise Exception(f"Operator {self.operator} could not be found")
    def __str__(self):
        return f"({self.left} {self.operator} {self.right})"
