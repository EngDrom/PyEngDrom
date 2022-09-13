

class UnknownCharacterException:
    def __init__(self, line, col, file):
        self.line = line
        self.col  = col
        self.file = file
    def make_message(self):
        return f"Unkown character at line {self.line} at col {self.col} in file {self.file}"

