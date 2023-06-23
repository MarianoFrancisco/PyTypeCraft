from ..Instruction.function import Function
from ..Semantic.exception import CompilerException

class Length(Function):
    def __init__(self, name, parameters, instructions, line, column):
        self.type="number"
        super().__init__(name, parameters, instructions, line, column)  
    
    def execute(self, tree, table):
        print('ejecutando lengthhhh')
        var=table.getSymbolById("length#parameter")
        if var == None: return CompilerException("Semantico", "No se encontro el parametro de length", self.line,self.column)
        if not (isinstance(var.value, str) or isinstance(var.value, list)):
            return CompilerException("Semantico", "La funcion length solo recibe arrays o strings como parametros", var.line, var.column)
        length=len(var.value)
        return length