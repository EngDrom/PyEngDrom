from org.pyengdrom.pydromadaire.parser.cursor import ParserCursor
from org.pyengdrom.pydromadaire.parser.grammar.parserrule import ParserRule

class TokenRule(ParserRule):
	def __init__ ( self, type, add_val, expected_value=None ):
		self.type    = type
		self.add_val = add_val

		self.expected_value = expected_value

	def parse(self, cursor : ParserCursor):
		if (
			cursor.get_cur_token().get_type() == self.type
			and (self.expected_value is None or self.expected_value == cursor.get_cur_token().get_value())
		):
			if ( self.add_val ):
				if ( cursor.get_cur_token().get_value() is not None ):
					cursor.addArgument(cursor.get_cur_token().get_value())
				else:
					cursor.addArgument(cursor.get_cur_token().get_type())
            
			cursor.tok_idx += 1
			return cursor.COMPILER_CONTINUE_NODE
		
		return cursor.COMPILER_ERR_NODE