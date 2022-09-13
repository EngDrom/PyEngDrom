from org.pyengdrom.pydromadaire.parser.grammar.parserrule import ParserRule
from org.pyengdrom.pydromadaire.parser.cursor import ParserCursor

class OptionnalRule ( ParserRule ):
	def __init__ (self, rule : ParserRule):
		self.rule = rule

	def parse(self, cursor : ParserCursor):
		n = self.rule.parse(cursor)
		if (n == cursor.COMPILER_ERR_NODE):
			return cursor.COMPILER_CONTINUE_BUTHADERR_NODE
		
		return n