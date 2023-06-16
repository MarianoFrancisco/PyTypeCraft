from ..Instruction.function import Function
from ..Semantic.exception import CompilerException

class Length(Function):
    def __init__(self, name, parameters, instructions, line, column):
        self.type="number"
        super().__init__(name, parameters, instructions, line, column)  
    
    def execute(self, tree, table):
        var=table.getSymbolById("split#parameter")
        separator=table.getSymbolById("split#parameter2")
        if var == None or separator==None: 
            return CompilerException("Semantico", "Faltan parametros en split", self.line,self.column)
        