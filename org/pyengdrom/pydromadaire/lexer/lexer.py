

from org.pyengdrom.pydromadaire.lexer.error import UnknownCharacterException


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
    
    def _build(self):
        if hasattr(self, "_built"): return self._built

        _built = []
        self.advance()

        while self.advanced:
            raise UnknownCharacterException(self.line, self.col, self.file)

        self._built = _built

        return self._built
