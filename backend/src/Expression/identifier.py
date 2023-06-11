from ..Symbol_Table.exception import CompilerException
from ..Abstract.abstract import Abstract


class Identificador(Abstract):
    def __init__(self, id, line, column, type=None):
        self.id = id
        self.line = line
        self.column = column
        self.type = type

    def interpret(self, tree, table):
        symbol = table.getTable(self.id)
        if symbol == None:
            return CompilerException("Semantico", "Variable no encontrada", self.line, self.column)
        self.type = symbol.getType()
        return symbol.getValue()
