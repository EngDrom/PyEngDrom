
from org.pyengdrom.pydromadaire.parser.cursor import ParserCursor
from org.pyengdrom.pydromadaire.parser.grammar.parserrule import ParserRule


class ManyRule(ParserRule):
	def __init__( self, rule : ParserRule, times_max : int, all_needed : bool ):
		self.rule       = rule
		self.times_max  = times_max
		self.all_needed = all_needed

	def parse(self, cursor : ParserCursor):
		cursor.save()
		
		idx = 0
		while (idx != self.times_max): # != to allow -1 for an infinite amount
			n = self.parse(cursor)
			
			if (n != cursor.COMPILER_CONTINUE_NODE):
				if (self.all_needed):
					cursor.restore()
					return cursor.COMPILER_ERR_NODE
                
				break

			idx += 1
		
		cursor.free(True)
		
		return None

