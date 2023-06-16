from ..Instruction.function import Function
from ..Semantic.exception import CompilerException

class ToString(Function):
    def __init__(self, name, parameters, instructions, line, column):
        self.type="string"
        super().__init__(name, parameters, instructions, line, column)  
    
    def execute(self, tree, table):
        symbol=table.getSymbolById("tostring#parameter")
        if symbol == None: return CompilerException("Semantico", "No se encontro el parametro de toString",self.line,self.column)
        toString= str(symbol.value)
        return toString