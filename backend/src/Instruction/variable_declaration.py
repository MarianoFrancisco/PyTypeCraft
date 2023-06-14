from ..Semantic.exception import CompilerException
from ..Abstract.abstract import Abstract
from ..Semantic.symbol import Symbol

class VariableDeclaration(Abstract):

    def __init__(self, id, type, value, line, column):
        self.id = id # a
        self.type = type # Number, String, Boolean
        self.value = value # 4, 'hola', true
        super().__init__(line, column)
    
    def interpretar(self, arbol, tabla):
        value = self.value.interpretar(arbol, tabla)
        if isinstance(value, CompilerException): return value # Analisis Semantico -> Error
        # Verificacion de types
        if str(self.type) == str(self.value.type):
            simbolo = Symbol(str(self.id), self.value.type, value, self.line, self.column)
            result = tabla.setTabla(simbolo)
            if isinstance(result, CompilerException): return result
            return None
        else:
            result = CompilerException("Semantico", "type de dato diferente declarado.", self.line, self.column)
            return result