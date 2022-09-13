
from typing import List

class Operator:
    def __init__(self, character, type, childrens=[]):
        self.chr  = character
        self.next = childrens
        self.type = type
    def is_valid(self, lexer, depth):
        return lexer._next(depth - 1) == self.chr
    def get_next(self, lexer, depth):
        for next in self.next:
            if next.is_valid(lexer, depth):
                return next
        
        return None
    def get_token(self):
        return self.type
