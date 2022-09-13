

class UnknownCharacterException(BaseException):
    def __init__(self, line, col, file):
        self.line = line
        self.col  = col
        self.file = file

        super().__init__(self.make_message())
    def __str__(self): return self.make_message()
    def make_message(self):
        return f"Unkown character at line {self.line} at col {self.col} in file {self.file}"

