
from org.pyengdrom.pydromadaire.lexer.token import Token

class VariableStack:
    NO_VAR = Token(None)

    def __init__(self, __global__ : "VariableStack"=None):
        self.dict        = {}
        self.global_vars = set()
        self.__global__  = __global__
    def __getitem__(self, idx):
        assert isinstance(idx, str)

        if idx in self.dict: return self.dict[idx] # TODO include heap based system
        if self.__global__ : raise  Exception("Could not find variable", idx)

        self.global_vars.add(idx)
        return self.__global__[idx]
    def __setitem__(self, idx, value):
        assert isinstance(idx, str)
        print(idx, value)
        if idx in self.global_vars:
            self.__global__.__setitem__(idx, value)
        else:
            self.dict[idx] = value