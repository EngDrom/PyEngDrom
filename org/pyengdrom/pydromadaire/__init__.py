
from org.pyengdrom.pydromadaire.evaluate.nodes.block import BlockNode
from org.pyengdrom.pydromadaire.evaluate.stack import VariableStack
from org.pyengdrom.pydromadaire.lexer.lexer   import Lexer
from org.pyengdrom.pydromadaire.parser.config import PyDromConfig
from org.pyengdrom.pydromadaire.parser.cursor import ParserCursor
from org.pyengdrom.pydromadaire.parser.grammar.rules.block import BlockRule

import pdb

class PyDromLangage:
    conf = PyDromConfig()

    @staticmethod
    def compile(string, file):
        lexer  = Lexer(string, file)
        tokens = lexer._build()

        rule = PyDromLangage.conf.get_block_rule()

        cursor = ParserCursor(tokens)
        cursor.set_config(PyDromLangage.conf)

        rule.parse(cursor, False)
        
        return cursor.args()[0]
    @staticmethod
    def run(node : BlockNode):
        node.evaluate(None, True)
    @staticmethod
    def run_module(node: BlockNode, data={}):
        global_stack = VariableStack(None)
        global_stack.__setitem__("print", print)

        stack = VariableStack(global_stack)
        for key in data:
            global_stack[key] = data[key]
        node.evaluate(stack, False)
        return stack