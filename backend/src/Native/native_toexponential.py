from ..Semantic.exception import CompilerException
from ..Instruction.function import Function

class ToExponential(Function):

    def __init__(self, name, parameters, instructions, line, column):
        self.type="string"
        super().__init__(name, parameters, instructions, line, column)
    
    def execute(self, tree, table):
        var = table.getSymbolById("toexponential#parameter")
        exponential = table.getSymbolById("toexponential#parameter2")
        if exponential == None or var == None:
            return CompilerException("Semantico", "Faltan parametros en toExponential ", self.line, self.column)
        data_exponential = "{:.{}e}".format(var.value, exponential.value)
        return data_exponential