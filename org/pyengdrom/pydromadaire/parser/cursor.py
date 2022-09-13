from typing import List
from org.pyengdrom.pydromadaire.lexer.token import Token

class ParserCursor:
    COMPILER_CONTINUE_NODE = Token(None)
    COMPILER_ERR_NODE      = Token(None)

    COMPILER_CONTINUE_BUTHADERR_NODE = Token(None)

    tok_idx = 0
    saves: List[int] = []
    tokens: List[Token] = []
    arguments: List = []
    args_saves: List[int] = []

    config = None
    def set_config(self, config):
        self.config = config

    def args(self) -> List:
        if len(self.args_saves) == 0:
            return self.arguments
        return self.arguments[self.args_saves[-1] :]

    def __init__(self, tokens):
        self.tokens = tokens

    def save(self):
        self.saves.append(self.tok_idx)
        self.args_saves.append(len(self.arguments))

    def free(self, found):
        if not found:
            self.restore()
        else:
            self.saves.pop()
            self.args_saves.pop()

    def get_cur_token(self):
        return self.tokens[self.tok_idx]

    def restore(self):
        if self.saves.size() == 0:
            self.tok_idx = 0
        else:
            self.tok_idx = self.saves[-1]
            self.saves.pop()

        if len(self.arguments) == 0:
            self.arguments.clear()
        else:
            rst = self.args_saves[-1]
            self.args_saves.pop()
            while rst < len(self.arguments):
                self.arguments.pop()

    def addArgument(self, obj):
        self.arguments.append(obj)

    def token_count(self):
        return len(self.tokens)

    def restore_arguments(self):
        rst = self.args_saves[-1]
        while rst < len(self.arguments):
            self.arguments.pop()
