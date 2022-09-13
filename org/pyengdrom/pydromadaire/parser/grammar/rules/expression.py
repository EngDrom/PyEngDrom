
from typing import List
from org.pyengdrom.pydromadaire.parser.grammar.parserrule import ParserRule
from org.pyengdrom.pydromadaire.parser.cursor import ParserCursor

OperatorNode = lambda a,b : None

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
            value = self.addition()

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
        '''
        if (tok.type == NUMBER):
            return new IntNode(tok.value)
        else if (tok.type == TokenType.NAME):
            if (self.cursor.get_cur_token().type == TokenType.SET):
                self.cursor.tok_idx += 1
                return new SetNode(new Object[]:
                    tok.value,
                    self.addition()
                )
            

            return new GetNode(tok.value)
        '''
        
        # raise InnerExpressionException()
        return None
    


