from ..Instruction.function import Function
from ..Semantic.exception import CompilerException

class ToLowerCase(Function):
    def __init__(self, name, parameters, instructions, line, column):
        self.type="string"
        super().__init__(name, parameters, instructions, line, column)  
    
    def execute(self, tree, table):
        var=table.getSymbolById("tolowercase#parameter")
        if var == None: return CompilerException("Semantico", "No se encontro el parametro de toLowerCase",self.line,self.column)
        toLowerCase= var.value.lower()
        return toLowerCase