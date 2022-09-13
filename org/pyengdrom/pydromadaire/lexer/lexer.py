
class Lexer:
    idx      = -1
    advanced = False
    chr      = ''

    col  = 0
    line = 1

    def __init__(self, string, file):
        self.string = string
        self.file   = file
    def advance(self):
        return self._move(1)
    def next(self):
        return self._next(1)
    
    def _move(self, delta):
        assert delta >= 0, "[LEXER] - Negative delta not allowed"
        
        substring = self.string[self.idx : self.idx + delta]
        newlines  = substring.count("\n")
        idx_l_new = substring.index("\n") if newlines != 0 else -1

        self.line += newlines
        self.idx  += delta

        self.col  += delta
        if idx_l_new != -1:
            self.col  = delta - idx_l_new
        
        self.advanced = self.idx < len(self.string)
        self.chr      = self.string[self.idx] if self.advanced else ''

        return self.advanced
    def _next(self, delta):
        nidx = self.idx + delta
        if len(self.string) > nidx >= 0: return self.string[nidx]

        return None
    
    def _bundle(self, **kwargs):
        return {
            **kwargs,
            "col"  : self.col,
            "line" : self.line,
            "file" : self.file
        }
    def _make(self, _built, _type, _size):
        _built.append( 
            Token(
                (_type, self.string[self.idx : self.idx + _size]),
                **self._bundle(size=_size)
            )
        )
        self._move(_size)
    def _build(self):
        if hasattr(self, "_built"): return self._built

        _built = []
        self.advance()

        while self.advanced:
            oper_data = self.make_operand()
            if oper_data is not None:
                self._make(_built, *oper_data)
                continue
            
            num_data = self.make_number()
            if num_data is not None:
                self._make(_built, *num_data)
                continue
            
            name_data = self.make_name()
            if name_data is not None:
                self._make(_built, *name_data)
                continue
                
            if self.chr in IGNORE_STRING:
                self.advance()
                continue

            raise UnknownCharacterException(self.line, self.col, self.file)

        self._built = _built

        return self._built
    def make_name  (self):
        if not self.chr in START_NAME_STRING: return None

        _size = 1
        while self._next(_size) in NAME_STRING: _size += 1

        return NAME, _size
    def make_number(self):
        if not self.chr in "0123456789": return None
        
        _size = 1
        while self._next(_size) in "0123456789": _size += 1

        if self._next(_size) == '.':
            _size += 1
            while self._next(_size) in "0123456789": _size += 1
        
        return NUMBER, _size
    def make_operand(self):
        operand = None
        depth   = 1

        for child in OPERAND_TREE:
            if child.is_valid(self, depth):
                operand = child
                break
        
        if operand is None: return None
        
        while True:
            depth += 1
            next   = operand.get_next(self, depth)
            if next is None: break

            operand = next
        
        token = operand.get_token()
        if token is None: return None

        return token, depth - 1

from org.pyengdrom.pydromadaire.lexer.config import IGNORE_STRING, NAME, NAME_STRING, NUMBER, OPERAND_TREE, START_NAME_STRING
from org.pyengdrom.pydromadaire.lexer.error import UnknownCharacterException
from org.pyengdrom.pydromadaire.lexer.token import Token