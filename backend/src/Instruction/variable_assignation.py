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
        if self.value.type != symbol.type:
            return CompilerException('Semantico', f'El valor {valueResult} no coincide con el tipo {symbol.type} de la variable {self.id}')
        
        result = table.updateSymbol(self.id, valueResult)
        if isinstance(result, CompilerException):
            return result
        return None