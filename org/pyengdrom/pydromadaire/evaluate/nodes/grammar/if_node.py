
from org.pyengdrom.pydromadaire.evaluate.nodes.block import BlockNode
from org.pyengdrom.pydromadaire.evaluate.nodes.node import EvaluatorNode
from org.pyengdrom.pydromadaire.evaluate.stack import VariableStack

class IfNode(EvaluatorNode):
    def __init__(self, *args):
        self.if_data = args[:2]
        args = args[2:]

        self.else_if_data = args[:(len(args) >> 1) << 1]
        self.else_data = None if (len(args) & 1) == 0 else args[-1]
    def can_if(self, stack : "VariableStack"):
        return self.is_true(self.eval(self.if_data[0], stack))
    def can_else_if(self, i, stack : "VariableStack"):
        return self.is_true(self.eval(self.else_if_data[i], stack))
    def _evaluate(self, block, stack: "VariableStack"):
        if block is None: return None
        if isinstance(block, BlockNode):
            return block.evaluate(stack)
        
        return self.eval(block, stack)
    def evaluate(self, stack: "VariableStack"):
        if self.can_if(stack): return self._evaluate(self.if_data[1], stack)
        for i in range(0, len(self.else_if_data), 2):
            if self.can_else_if(i, stack):
                return self._evaluate(self.else_if_data[i + 1], stack)
        return self._evaluate(self.else_data, stack)
