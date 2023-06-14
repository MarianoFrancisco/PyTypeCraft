from ..Semantic.exception import CompilerException
from ..Abstract.abstract import Abstract
from ..Semantic.symbol import Symbol

class VariableDeclaration(Abstract):

    def __init__(self, id, type, value, line, column):
        self.id = id # a
        self.type = type # Number, String, Boolean
        self.value = value # 4, 'hola', true
        super().__init__(line, column)
    
    def execute(self, tree, table):
        value = self.value.execute(tree, table)
        if isinstance(value, CompilerException): return value # Analisis Semantico -> Error
        # Verificacion de types
        if str(self.type) == str(self.value.type):
            symbol = Symbol(str(self.id), self.value.type, value, self.line, self.column)
            result = table.setTable(symbol)
            if isinstance(result, CompilerException): return result
            return None
        else:
            result = CompilerException("Semantico", "Tipo de dato diferente declarado.", self.line, self.column)
            return result