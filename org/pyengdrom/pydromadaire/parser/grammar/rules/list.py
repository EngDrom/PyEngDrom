
from typing import List
from org.pyengdrom.pydromadaire.parser.grammar.parserrule import ParserRule
from org.pyengdrom.pydromadaire.parser.cursor import ParserCursor

class ListRule (ParserRule):
    wrapper = None

    def __init__(self, sub_rules : List[ParserRule]):
        self.sub_rules = sub_rules
    
    def parse(self, cursor : ParserCursor):
        cursor.save()
        
        for sr in self.sub_rules:
            n = sr.parse(cursor)
            if (n == cursor.COMPILER_ERR_NODE):
                cursor.restore()
                return n
        
        if (self.wrapper != None):
            data = self.get_linked(cursor)
            cursor.restore_arguments()
            cursor.free(True)
            cursor.addArgument(data)
            return data
        

        cursor.free(True)
        return cursor.COMPILER_CONTINUE_NODE
    
    def get_linked(self, cursor : ParserCursor):
        return self.wrapper(*cursor.args())
    
    def link(self, wrapper):
        self.wrapper = wrapper
        return self
    
    
