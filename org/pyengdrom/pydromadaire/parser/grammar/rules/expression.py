
from typing import List
from org.pyengdrom.pydromadaire.evaluate.nodes.arraybuilder import ArrayBuilder
from org.pyengdrom.pydromadaire.evaluate.nodes.attr import CallFunctionNode, GetAtNode, GetNode, SetNode
from org.pyengdrom.pydromadaire.evaluate.nodes.operator import OperatorNode, UnaryNode
from org.pyengdrom.pydromadaire.lexer.config import COMMA, LBRACKET, LSQUARED_BRACKET, MINUS, NAME, NOT, NUMBER, RBRACKET, RSQUARED_BRACKET, SET
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
    
    def factor(self):
        left = self._factor()
        if self.cursor.get_cur_token().get_type() == SET:
            self.cursor.tok_idx += 1
            right = self.operator_priority(0)

            return SetNode(left, right)
        else: return left
    
    def _factor(self):
        left = self.factor_term()
        
        found = True
        while found:
            found = False
            while self.cursor.get_cur_token().get_type() == LSQUARED_BRACKET:
                self.cursor.tok_idx += 1
                index = self.operator_priority(0)
                if self.cursor.get_cur_token().get_type() != RSQUARED_BRACKET:
                    raise Exception("Expected ] after index [")
                self.cursor.tok_idx += 1
                left = GetAtNode(left, index)
                found = True
            
            while self.cursor.get_cur_token().get_type() == LBRACKET:
                self.cursor.tok_idx += 1

                args = []
                while self.cursor.get_cur_token().get_type() != RBRACKET:
                    args.append(self.operator_priority(0))

                    if self.cursor.get_cur_token().get_type() == COMMA:
                        self.cursor.tok_idx += 1
                        continue
                    if self.cursor.get_cur_token().get_type() == RBRACKET:
                        self.cursor.tok_idx += 1
                        break

                    raise Exception("Expected closing bracket or comma")

                if len(args) == 0: self.cursor.tok_idx += 1

                left  = CallFunctionNode(left, args)
                found = True
        
        return left
    def factor_term (self):
        tok = self.get_cur_token()
        self.cursor.tok_idx += 1

        if tok.get_type() in [NOT, MINUS]:
            return UnaryNode(self.factor_term(), tok.get_type())
        
        if (tok.get_type() == NUMBER):
            return (float if '.' in tok.get_value() else int)(tok.get_value())
        elif (tok.get_type() == NAME):
            return GetNode(tok.get_value())
        elif (tok.get_type() == LSQUARED_BRACKET):
            expressions = [  ]
            while True:
                expressions.append(self.operator_priority(0))
                
                if self.cursor.get_cur_token().get_type() == COMMA:
                    self.cursor.tok_idx += 1
                    continue
                if self.cursor.get_cur_token().get_type() == RSQUARED_BRACKET:
                    self.cursor.tok_idx += 1
                    break

                raise Exception("Expected closing squared bracket or comma")
            
            return ArrayBuilder(expressions)
        
        raise Exception("Could not find factor for", tok.get_value())
