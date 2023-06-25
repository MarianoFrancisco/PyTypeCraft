from ..Instruction.function import Function
from ..Semantic.exception import CompilerException

class ToUpperCase(Function):
    def __init__(self, name, parameters, instructions, line, column):
        super().__init__(name, parameters, instructions, line, column, 'string')  
    
    def execute(self, tree, table):
        var=table.getSymbolById("touppercase#parameter")
        if var == None: return CompilerException("Semantico", "No se encontro el parametro de toUpperCase",self.line,self.column)
        if var.type != "string":
            return CompilerException("Semantico", "En toUpperCase no puede ir otra variable que no sea string", self.line, self.column)
        toUpperCase= var.value.upper()
        return toUpperCase