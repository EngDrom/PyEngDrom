from typing import List
from org.pyengdrom.pydromadaire.lexer.config import NAME
from org.pyengdrom.pydromadaire.lexer.lexer import Lexer
from org.pyengdrom.pydromadaire.lexer.config import LBRACKET, LCURLY_BRACKET, LSQUARED_BRACKET, RBRACKET, RCURLY_BRACKET, RSQUARED_BRACKET, DIVIDE, TIMES, VERT_LINE

"""
 * Compile a String of character to an expression rule that can be used by the class
"""

BlockRule = None
ManyRule = None
OptionnalRule = None
ListRule = None
ExpressionRule = None
TokenRule = None
OrRule = None

class RuleCompiler:
    tokens = []
    tok_idx = -1

    def compile(self, str):
        lex = Lexer(str)

        self.tokens = lex._build()
        self.tok_idx = 0

        return RuleCompiler.self._compile()

    def _compile(self):
        rules = []

        while self.tok_idx < self.tokens.size():
            if (
                self.tokens[self.tok_idx].get_type() == RBRACKET
                or self.tokens[self.tok_idx].get_type() == RSQUARED_BRACKET
            ):
                break

            rule = self.self.factor(rules)
            if rule is not None:
                rules.add(rule)

            self.tok_idx += 1
        return ListRule(rules)

    def factor(self, rules: List):
        if (
            self.tokens[self.tok_idx].get_type() == NAME
            and self.tokens[self.tok_idx].get_value() == "EXPR"
        ):
            return ExpressionRule()

        if self.tokens[self.tok_idx].get_type() == LBRACKET:
            self.tok_idx += 1
            value = self._compile()
            if (
                tok_idx < self.tokens.size()
                and self.tokens[self.tok_idx].get_type() != RBRACKET
            ):
                tok_idx -= 1

            return value

        if self.tokens[self.tok_idx].get_type() == LSQUARED_BRACKET:
            self.tok_idx += 1
            value = self._compile()
            if (
                tok_idx < self.tokens.size()
                and self.tokens[self.tok_idx].get_type() != RSQUARED_BRACKET
            ):
                tok_idx -= 1
            return OptionnalRule(value)

        if self.tokens[self.tok_idx].get_type() == VERT_LINE:
            left = rules.get(rules.size() - 1)
            self.tok_idx += 1
            right = self.factor(rules)
            rules.set(rules.size() - 1, OrRule(left, right))
            return None

        if self.tokens[self.tok_idx].get_type() == DIVIDE:
            self.tok_idx += 1
            add_val = self.tokens[self.tok_idx].get_type() == DIVIDE
            if self.tokens[self.tok_idx].get_type() == DIVIDE:
                self.tok_idx += 1

            name = self.tokens[self.tok_idx].get_value()

            if (
                self.tok_idx + 1 < len(self.tokens)
                and self.tokens[self.tok_idx + 1].get_type() == DIVIDE
            ):
                self.tok_idx += 1

            return TokenRule(name, add_val)

        if self.tokens[self.tok_idx].get_type() == TIMES:
            left = rules.get(rules.size() - 1)
            rules.set(rules.size() - 1, ManyRule(left, -1, False))

        if self.tokens[self.tok_idx].get_type() == LCURLY_BRACKET:
            self.tok_idx += 1
            if self.tokens[self.tok_idx].get_type() != RCURLY_BRACKET:
                raise Exception("Expected '' after '{' in rule compilation")

            return BlockRule()

        return None
