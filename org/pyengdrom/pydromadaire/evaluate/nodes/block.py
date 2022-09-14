

from typing import List
from org.pyengdrom.pydromadaire.evaluate.nodes.node import EvaluatorNode
from org.pyengdrom.pydromadaire.evaluate.stack import VariableStack

class BlockNode(EvaluatorNode):
    def __init__(self, nodes : List):
        self.nodes = nodes
    def evaluate(self, stack: "VariableStack", make_stack=False):
        if make_stack: stack = VariableStack(
            stack.__global__ if stack is not None else None
        )

        for node in self.nodes:
            if isinstance(node, EvaluatorNode):
                node.evaluate(stack)
