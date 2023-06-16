from ..Instruction.function import Function
from ..Semantic.exception import CompilerException

class Split(Function):
    def __init__(self, name, parameters, instructions, line, column):
        self.type="string"
        super().__init__(name, parameters, instructions, line, column)  
    
    def execute(self, tree, table):
        var=table.getSymbolById("split#parameter")
        separator=table.getSymbolById("split#parameter2")
        if var == None or separator==None: 
            return CompilerException("Semantico", "Faltan parametros en split", self.line,self.column)
        self.type=var.type
        print(self.type)
        array_split=var.value.split(separator.value)
        return array_split