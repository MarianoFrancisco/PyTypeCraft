from ..Expression.array import Array
from ..Semantic.symbol import Symbol, AnySymbol, ArraySymbol
from ..Semantic.exception import CompilerException
from ..Abstract.abstract import Abstract


class VariableAssignation(Abstract):
    def __init__(self, id, value, line, column):
        super().__init__(line, column)
        self.id = id
        self.value = value

    def execute(self, tree, table):
        valueResult = self.value.execute(tree, table)
        if isinstance(valueResult, CompilerException): return valueResult
        symbol = table.getSymbolById(self.id)
        if isinstance(symbol, CompilerException): return symbol
        if not isinstance(symbol, AnySymbol) and self.value.type != symbol.type:
            return CompilerException('Semantico', f'El valor {valueResult} no coincide con el tipo {symbol.type} de la variable {self.id}', self.line, self.column)
        
        if isinstance(symbol, ArraySymbol) and not isinstance(self.value, Array):
            return CompilerException("Semantico", f"La expresion {valueResult} no puede asignarse a '{self.id}', ya que no es un arreglo", self.line, self.column)
        if not isinstance(symbol, AnySymbol) and not isinstance(symbol, ArraySymbol) and isinstance(self.value, Array):
            return CompilerException("Semantico", f"La variable '{self.id}' no se le puede asignar un arreglo", self.line, self.column)
        symbolUpdated = Symbol(self.id, self.value.type, valueResult, self.line, self.column)
        
        if isinstance(symbol, AnySymbol) and isinstance(self.value, Array):
            symbol.type = f'Array<{self.value.type}>'
        result = table.updateSymbol(symbolUpdated)
        if isinstance(result, CompilerException):
            return result
        return None