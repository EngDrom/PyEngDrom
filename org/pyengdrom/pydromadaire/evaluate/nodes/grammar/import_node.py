
import os

from org.pyengdrom.pydromadaire.evaluate.nodes.node import EvaluatorNode
from org.pyengdrom.pydromadaire.evaluate.stack import VariableStack

import importlib
import org.pyengdrom.api.engine

python_std_forward = [ 'math', 'time', 'random' ]

class ImportNode(EvaluatorNode):
    def __init__(self, *args):
        self.module = os.path.join(args[0], *args[1:])
    def evaluate(self, stack: "VariableStack"):
        if self.module in python_std_forward:
            stack[self.module] = importlib.__import__(self.module)
        elif self.module == "engdrom": # Import engdrom dmd api
            stack.__global__["engdrom"] = org.pyengdrom.api.engine.EngDromAPI
        else:
            print("loading custom module : ", self.module)

