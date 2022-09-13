
from typing import List
from org.pyengdrom.pydromadaire.parser.grammar.parserrule import ParserRule
from org.pyengdrom.pydromadaire.parser.cursor import ParserCursor
from org.pyengdrom.pydromadaire.lexer.config import LCURLY_BRACKET, RCURLY_BRACKET, EOF

BlockNode = lambda x : None

class BlockRule (ParserRule):
    def parse(cursor : ParserCursor, bracketBased=True):
        if bracketBased:
            if (cursor.get_cur_token().get_type() != LCURLY_BRACKET):
                return cursor.COMPILER_ERR_NODE
            cursor.tok_idx += 1

        nodes = []

        cursor.save()

        while (cursor.tok_idx < cursor.token_count()):
            if (cursor.get_cur_token().type == RCURLY_BRACKET):
                break

            if (cursor.get_cur_token().type == EOF):
                cursor.tok_idx += 1
                continue
            
            final_node = None
            for rule in cursor.config.get_rule_list():
                node = rule.parse(cursor)

                if (node == cursor.COMPILER_ERR_NODE):
                    continue

                final_node = node
                break
            

            if (final_node is not None):
                nodes.append(final_node)
            else:
                cursor.restore()
                return cursor.COMPILER_ERR_NODE
            

            if (cursor.tok_idx >= cursor.token_count() 
             or  (cursor.get_cur_token().get_type() != EOF
             and  cursor.get_cur_token().get_type() != RCURLY_BRACKET)):
                cursor.restore()
                return cursor.COMPILER_ERR_NODE
            
            if ((not bracketBased) and cursor.get_cur_token().get_type() == RCURLY_BRACKET):
                cursor.restore()
                return cursor.COMPILER_ERR_NODE

        if (bracketBased):
            if (cursor.get_cur_token().type != RCURLY_BRACKET):
                cursor.restore()
                return cursor.COMPILER_ERR_NODE
            
            cursor.tok_idx += 1
        

        cursor.restore_arguments()
        cursor.free(True)

        cursor.addArgument( BlockNode(nodes) )

        return cursor.COMPILER_CONTINUE_NODE
    

