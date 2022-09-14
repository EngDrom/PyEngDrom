
from typing import List
from org.pyengdrom.pydromadaire.evaluate.nodes.attr import GetNode, SetNode
from org.pyengdrom.pydromadaire.evaluate.nodes.operator import OperatorNode
from org.pyengdrom.pydromadaire.lexer.config import NAME, NUMBER, SET
from org.pyengdrom.pydromadaire.parser.grammar.parserrule import ParserRule
from org.pyengdrom.pydromadaire.parser.cursor import ParserCursor


class ExpressionException(BaseException):
    pass

class ExpressionRule (ParserRule):
    def __init__(self, stack : List[List[str]]):
        self.stack = stack
    
    cursor : ParserCursor = None
    def get_cur_token(self):
        return self.cursor.get_cur_token()

    def parse(self, cursor : ParserCursor):
        self.cursor = cursor
        cursor.save()
        
        try:
            value = self.operator_priority(0)

            self.cursor = None
            cursor.free(True)
            cursor.addArgument(value)
            return cursor.COMPILER_CONTINUE_NODE
        except ExpressionException as exception: 
            pass

        self.cursor = None
        cursor.free(False)
        return cursor.COMPILER_ERR_NODE
    
    def operator_priority (self, stack):
        if stack == len(self.stack): return self.factor()
        types = self.stack[stack]

        left = self.operator_priority(stack + 1)
        
        while self.get_cur_token().get_type() in types:
            operator = self.get_cur_token().get_type()
            self.cursor.tok_idx += 1
            
            right = self.operator_priority(stack + 1)
            left  = OperatorNode(left, right, operator)
        
        return left
    
    def factor (self):
        tok = self.get_cur_token()
        self.cursor.tok_idx += 1
        
        if (tok.get_type() == NUMBER):
            return (float if '.' in tok.get_value() else int)(tok.get_value())
        elif (tok.get_type() == NAME):
            if (self.cursor.get_cur_token().get_type() == SET):
                self.cursor.tok_idx += 1
                return SetNode(
                    tok.get_value(),
                    self.operator_priority(0)
                )
            
            return GetNode(tok.get_value())
        
        raise Exception("Could not find factor for", tok.get_value())
