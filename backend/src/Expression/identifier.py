from ..Semantic.exception import CompilerException
from ..Abstract.abstract import Abstract


class Identifier(Abstract):
    def __init__(self, id, line, column, type=None):
        self.id = id
        self.line = line
        self.column = column
        self.type = type

    def execute(self, tree, table):
        symbol = table.getSymbolById(self.id)
        if symbol == None:
            return CompilerException("Semantico", f"Variable no encontrada {self.id}", self.line, self.column)
        self.type = symbol.type
        return symbol.value

# llamando valores que sean de un array a traves de sus indices PENDIENTE DE IMPLEMENTAR
class IdentifierArray(Abstract):
    def __init__(self, id, line, column, indexes, type=None):
        self.id = id
        self.line = line
        self.column = column
        self.indexes = indexes
        self.type = type

    def execute(self, tree, table):
        symbol = table.getSymbolById(self.id)
        if symbol == None:
            return CompilerException("Semantico", f"Variable no encontrada {self.id}", self.line, self.column)
        self.type = symbol.type
        arr = symbol.value
        # if not isinstance(symbol, ArraySymbol)

        try:
            for index in self.indexes:
                result = index.execute(tree, table)

                arr = arr[result]
        except (IndexError, TypeError):
            return 'error'
        else:
            return arr
