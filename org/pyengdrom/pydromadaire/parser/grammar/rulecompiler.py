from typing import List

"""
 * Compile a String of character to an expression rule that can be used by the class
"""

class RuleCompiler:
    tokens = []
    tok_idx = -1

    def compile(self, str, config): # ParserConfig
        self.config = config
        lex = Lexer(str, "<std:rulecompiler>")

        self.tokens = lex._build()
        self.tok_idx = 0

        return self._compile()

    def _compile(self):
        rules = []

        while self.tok_idx < len(self.tokens):
            if (
                self.tokens[self.tok_idx].get_type() == RBRACKET
                or self.tokens[self.tok_idx].get_type() == RSQUARED_BRACKET
            ):
                break

            rule = self.factor(rules)
            if rule is not None:
                rules.append(rule)

            self.tok_idx += 1
        return ListRule(rules)

    def factor(self, rules: List):
        if (
            self.tokens[self.tok_idx].get_type() == NAME
            and self.tokens[self.tok_idx].get_value() == "EXPR"
        ):
            return self.config.get_expr_rule()

        if self.tokens[self.tok_idx].get_type() == LBRACKET:
            self.tok_idx += 1
            value = self._compile()
            if (
                self.tok_idx < len(self.tokens)
                and self.tokens[self.tok_idx].get_type() != RBRACKET
            ):
                self.tok_idx -= 1

            return value

        if self.tokens[self.tok_idx].get_type() == LSQUARED_BRACKET:
            self.tok_idx += 1
            value = self._compile()
            if (
                self.tok_idx < len(self.tokens)
                and self.tokens[self.tok_idx].get_type() != RSQUARED_BRACKET
            ):
                self.tok_idx -= 1
            return OptionnalRule(value)

        if self.tokens[self.tok_idx].get_type() == VERT_LINE:
            left = rules[-1]
            self.tok_idx += 1
            right = self.factor(rules)
            rules[-1] = OrRule(left, right)
            return None

        if self.tokens[self.tok_idx].get_type() == DIVIDE:
            self.tok_idx += 1
            add_val = self.tokens[self.tok_idx].get_type() == DIVIDE
            if self.tokens[self.tok_idx].get_type() == DIVIDE:
                self.tok_idx += 1

            name = self.tokens[self.tok_idx].get_value()
            expected_value = None
            if (
                self.tok_idx + 2 < len(self.tokens)
                and self.tokens[self.tok_idx + 1].get_type() == SET
            ):
                self.tok_idx += 2
                expected_value = self.tokens[self.tok_idx].get_value()

            if (
                self.tok_idx + 1 < len(self.tokens)
                and self.tokens[self.tok_idx + 1].get_type() == DIVIDE
            ):
                self.tok_idx += 1

            return TokenRule(name, add_val, expected_value)

        if self.tokens[self.tok_idx].get_type() == TIMES:
            left = rules[-1]
            rules[-1] = ManyRule(left, -1, False)
            
            return None

        if self.tokens[self.tok_idx].get_type() == LCURLY_BRACKET:
            self.tok_idx += 1
            if self.tokens[self.tok_idx].get_type() != RCURLY_BRACKET:
                raise Exception("Expected '' after '{' in rule compilation")

            return BlockRule()

        return None

from org.pyengdrom.pydromadaire.lexer.config import NAME
from org.pyengdrom.pydromadaire.lexer.lexer import Lexer
from org.pyengdrom.pydromadaire.lexer.config import LBRACKET, LCURLY_BRACKET, LSQUARED_BRACKET, RBRACKET, RCURLY_BRACKET, RSQUARED_BRACKET, DIVIDE, TIMES, VERT_LINE
from org.pyengdrom.pydromadaire.parser.grammar.rules import *
