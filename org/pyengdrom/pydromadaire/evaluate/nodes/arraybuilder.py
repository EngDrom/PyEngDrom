

from org.pyengdrom.pydromadaire.evaluate.nodes.node import EvaluatorNode
from org.pyengdrom.pydromadaire.evaluate.stack import VariableStack

class ArrayBuilder(EvaluatorNode):
    def __init__(self, expressions):
        self.expressions = expressions
    def evaluate(self, stack: "VariableStack"):
        return list(map(lambda x : self.eval(x, stack), self.expressions))
    def __str__(self):
        return "[ " + ", ".join(map(str, self.expressions)) + " ]"

