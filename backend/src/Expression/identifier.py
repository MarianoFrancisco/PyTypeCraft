from ..Semantic.exception import CompilerException
from ..Abstract.abstract import Abstract


class Identifier(Abstract):
    def __init__(self, id, line, column, type=None):
        self.id = id
        self.line = line
        self.column = column
        self.type = type

    def execute(self, tree, table):
        symbol = table.getTable(self.id)
        if symbol == None:
            return CompilerException("Semantico", f"Variable no encontrada {self.id}", self.line, self.column)
        self.type = symbol.type
        return symbol.value
