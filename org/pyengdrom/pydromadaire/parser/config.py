
from typing import List
from org.pyengdrom.pydromadaire.evaluate.nodes.grammar.function_node import FunctionBuilderNode
from org.pyengdrom.pydromadaire.evaluate.nodes.grammar.if_node import IfNode
from org.pyengdrom.pydromadaire.evaluate.nodes.grammar.while_node import WhileNode
from org.pyengdrom.pydromadaire.lexer.config import AND, B_AND, B_OR, DIVIDE, EQUALS, GREATER, LESS, MINUS, NOT, OR, PLUS, TIMES, XOR
from org.pyengdrom.pydromadaire.parser.grammar.parserrule import ParserRule
from org.pyengdrom.pydromadaire.parser.grammar.rulecompiler import BlockRule, RuleCompiler
from org.pyengdrom.pydromadaire.parser.grammar.rules.expression import ExpressionRule

class ParserConfig:
    def __init__(self):
        pass
    def get_expr_rule(self):
        raise Exception("Default PC does not work")
    def get_rule_list(self) -> List[ParserRule]:
        raise Exception("Default PC does not work")

class PyDromConfig:
    def __init__(self):
        self.expr_rule = ExpressionRule([
            [XOR, OR, AND, B_OR, B_AND],
            [GREATER, LESS, GREATER + EQUALS, LESS + EQUALS, NOT + EQUALS, EQUALS],
            [PLUS, MINUS],
            [TIMES, DIVIDE]
        ])
        compiler = RuleCompiler()
        compiler.config = self

        self.rule_list = [
            compiler.compile(
                     "/NAME=if/ /LBRACKET/ EXPR /RBRACKET/ {}"
                    +"[/NAME=else/ /NAME=if/ /LBRACKET/ EXPR /RBRACKET/ {}]*"
                    +"[/NAME=else/ {}]",
                    self
                ).link(IfNode),
            compiler.compile(
                "/NAME=while/ /LBRACKET/ EXPR /RBRACKET/ {}",
                self
            ).link(WhileNode),
            compiler.compile(
                "/NAME=function/ //NAME/ /LBRACKET/ [//NAME/ [/COMMA/ //NAME/]*] /RBRACKET/ {}",
                self
            ).link(FunctionBuilderNode),
            ## WARING MUST BE LAST
            compiler.compile("EXPR", self).link(lambda x: x),
        ]
        self.block_rule = BlockRule()
    def get_expr_rule(self):
        return self.expr_rule
    def get_rule_list(self) -> List[ParserRule]:
        return self.rule_list
    def get_block_rule(self):
        return self.block_rule
