from ..Semantic.exception import CompilerException
from ..Instruction.function import Function

class ToFixed(Function):

    def __init__(self, name, parameters, instructions, line, column):
        self.type="number"
        super().__init__(name, parameters, instructions, line, column)
    
    def execute(self, tree, table):
        var = table.getSymbolById("tofixed#parameter")
        decimal = table.getSymbolById("tofixed#parameter2")
        if decimal == None or var == None:
            return CompilerException("Semantico", "Faltan parametros en ToFixed ", self.line, self.column)
        approximation = round(var.value,decimal.value)
        return approximation
    
    