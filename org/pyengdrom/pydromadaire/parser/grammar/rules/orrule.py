from org.pyengdrom.pydromadaire.parser.grammar.parserrule import ParserRule
from org.pyengdrom.pydromadaire.parser.cursor import ParserCursor

class OrRule (ParserRule):
	def __init__(self, left : ParserRule, right : ParserRule):
		self.left  = left
		self.right = right
	
	def parse(self, cursor : ParserCursor):
		n0 = self.left.parse(cursor)
		if (n0 != cursor.COMPILER_ERR_NODE):
			return n0
		
		cursor.restore()
		
		return self.right.parse(cursor)
	