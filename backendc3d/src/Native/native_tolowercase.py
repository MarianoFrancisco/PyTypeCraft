from ..Instruction.function import Function
from ..Semantic.exception import CompilerException

class ToLowerCase(Function):
    def __init__(self, name, parameters, instructions, line, column,type):
        super().__init__(name, parameters, instructions, line, column,type)  
    
    def execute(self, tree, table):
        return
        # var=table.getSymbolById("tolowercase#parameter")
        # if var == None: return CompilerException("Semantico", "No se encontro el parametro de toLowerCase",self.line,self.column)
        # toLowerCase= var.value.lower()
        # return toLowerCase