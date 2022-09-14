
from org.pyengdrom.pydromadaire.evaluate.nodes.block import BlockNode
from org.pyengdrom.pydromadaire.evaluate.nodes.node import EvaluatorNode
from org.pyengdrom.pydromadaire.evaluate.stack import VariableStack

class WhileNode(EvaluatorNode):
    def __init__(self, *args):
        self.condition = args[0]
        self.blocknode = args[1]
    def can_continue(self, stack: "VariableStack"):
        return self.is_true(self.eval(self.condition, stack))
    def _evaluate(self, block, stack: "VariableStack"):
        if block is None: return None
        if isinstance(block, BlockNode):
            return block.evaluate(stack)
        
        return self.eval(block, stack)
    def evaluate(self, stack: "VariableStack"):
        while self.can_continue(stack):
            data = self._evaluate(self.blocknode, stack)
            if data is not None:
                return data # TODO add continue and break
