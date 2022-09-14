
from org.pyengdrom.pydromadaire.evaluate.stack import VariableStack

class EvaluatorNode:
    def __init__(self):
        pass
    def evaluate(self, stack : "VariableStack"):
        raise Exception("Default EvaluatorNode not available")
    def is_true(self, x):
        return x == True or (isinstance(x, int) and x != 0)
    def eval(self, x, stack : "VariableStack"):
        while isinstance(x, EvaluatorNode): x = x.evaluate(stack)
        return x