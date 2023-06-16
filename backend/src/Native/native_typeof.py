from ..Instruction.function import Function
from ..Semantic.exception import CompilerException

class TypeOf(Function):
    def __init__(self, name, parameters, instructions, line, column):
        self.type="any"
        super().__init__(name, parameters, instructions, line, column)  
    
    def execute(self, tree, table):
        var=table.getSymbolById("typeof#parameter")
        if var == None: return CompilerException("Semantico", "No se encontro el parametro de TypeOf",self.line,self.column)
        self.type = self.getType(var.value)
        return self.type
    
    def getType(self, value):
        if type(value) == int or type(value)==float:
            return 'number'
        elif type(value)==str:
            return 'string'
        elif type(value)==bool:
            return 'boolean'