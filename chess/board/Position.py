class Position:

    def __init__(self, line, column):
        self._line = line
        self._column = column

    @property
    def line(self):
        return self._line

    @property
    def column(self):
        return self._column

    def __add__(self, other):
        if isinstance(other, Position):
            return Position(self.line + other.line, self.column + other.column)
        raise TypeError

    def __eq__(self, other):
        if isinstance(other, Position):
            return other.line == self.line and other.column == self.column
        return False

    def __repr__(self):
        return f"{self.__class__.__name__}(line: {self.line}, column: {self.column})"
