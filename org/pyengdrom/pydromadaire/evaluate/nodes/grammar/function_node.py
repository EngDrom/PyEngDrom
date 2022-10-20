

from org.pyengdrom.pydromadaire.evaluate.nodes.block import BlockNode
from org.pyengdrom.pydromadaire.evaluate.nodes.node import EvaluatorNode
from org.pyengdrom.pydromadaire.evaluate.stack import VariableStack

class FunctionBuilderNode(EvaluatorNode):
    def __init__(self, *args):
        self.name = args[0]
        self.func = args[-1]
        self.arg_names = args[1: -1]
        for arg_name in self.arg_names:
            if not isinstance(arg_name, str):
                raise Exception("Expected string as function argument")
    def evaluate(self, stack: "VariableStack"):
        function = FunctionNode(stack.__global__, self.arg_names, self.func)
        stack.__setitem__(self.name, function)

        return function

class FunctionNode:
    def __init__(self, __global__, arg_names, blocknode):
        self.__global__ = __global__
        self.blocknode  = blocknode
        self.arg_names  = arg_names
    def __call__(self, *args):
        if len(args) != len(self.arg_names): raise Exception(f"Expected {len(self.arg_name)} arguments, got {len(args)}")
        
        stack = VariableStack(self.__global__)
        for i in range(len(args)):
            stack.__setitem__(self.arg_names[i], args[i])
        
        return self._evaluate(self.blocknode, stack)
    def _evaluate(self, block, stack: "VariableStack"):
        if block is None: return None
        if isinstance(block, BlockNode):
            return block.evaluate(stack)
        
        return self.eval(block, stack)
