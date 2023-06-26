from ..Expression.array import Array
from ..Expression.primitive import Primitive
from ..Semantic.exception import CompilerException
from ..Abstract.abstract import Abstract
from ..Semantic.symbol import Symbol, ArraySymbol, AnySymbol

class VariableDeclaration(Abstract):

    def __init__(self, id, type, value, line, column):
        self.id = id # a
        self.type = type # Number, String, Boolean
        self.value = value # 4, 'hola', true
        super().__init__(line, column)
        # ASIGNANDO VALORES POR DEFECTO
        if value == None:
            if type == 'number':
                self.value = Primitive(0, 'number', self.line, self.column)
            elif type == 'boolean':
                self.value = Primitive(False, 'boolean', self.line, self.column)
            elif type == 'string':
                self.value = Primitive('', 'string', self.line, self.column)
            else:
                self.value = Primitive('', 'any', self.line, self.column)
    
    def execute(self, tree, table):
        value = self.value.execute(tree, table)
        if isinstance(value, CompilerException): return value # Analisis Semantico -> Error
        # Verificacion de types
        if '[]' in self.type and not isinstance(self.value, Array):
            return CompilerException("Semantico", f"La expresion {value} no puede asignarse a '{self.id}', ya que no es un arreglo", self.line, self.column)
        if self.type != 'any' and not ('[]' in self.type) and isinstance(self.value, Array):
            return CompilerException("Semantico", f"La variable '{self.id}' no se le puede asignar un arreglo", self.line, self.column)
        if 'any' in str(self.type) or str(self.value.type) in str(self.type):
            symbol = None
            if 'any' in self.type:
                symbol = AnySymbol(str(self.id), self.value.type, value, self.line, self.column)
            elif isinstance(self.value, Array):
                symbol = ArraySymbol(str(self.id), self.value.type, value, self.line, self.column)
            else:
                symbol = Symbol(str(self.id), self.value.type, value, self.line, self.column)
            result = table.addSymbol(symbol)
            if isinstance(result, CompilerException): return result
            return None
        else:
            result = CompilerException("Semantico", "Tipo de dato diferente declarado.", self.line, self.column)
            return result
    