
from typing import List
from org.pyengdrom.pydromadaire.lexer.config import DIVIDE, MINUS, PLUS, TIMES
from org.pyengdrom.pydromadaire.parser.grammar.parserrule import ParserRule
from org.pyengdrom.pydromadaire.parser.grammar.rulecompiler import RuleCompiler
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
            [PLUS, MINUS],
            [TIMES, DIVIDE]
        ])
        compiler = RuleCompiler()
        compiler.config = self

        self.rule_list = [
            compiler.compile("/NAME/ /NUMBER/", self).link(print)
        ]
    def get_expr_rule(self):
        return self.expr_rule
    def get_rule_list(self) -> List[ParserRule]:
        return self.rule_list
