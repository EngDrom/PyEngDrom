from org.pyengdrom.pydromadaire.lexer.type import LE_Token_Data, LE_Type, LE_Value


class Token:
    _data: LE_Token_Data = None

    def __str__(self):
        return str(self.get_type()) + ":" + str(self.get_value())

    def __init__(self, data: LE_Token_Data, **kwargs):
        self._data = data

        for key in kwargs.keys():
            setattr(self, key, kwargs[key])

    def get_type(self) -> LE_Type:
        return self._data[0]

    def get_value(self) -> LE_Value:
        return self._data[1]
