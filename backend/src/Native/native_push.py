from ..Semantic.exception import CompilerException
from ..Instruction.function import Function
from ..Semantic.symbol import Symbol

class Push(Function):

    def __init__(self, name, parameters,instructions, line,column):
        super().__init__(name, parameters,instructions, line,column)
    
    def execute(self, tree, table):
        array = table.getSymbolById("push#parameter")
        data = table.getSymbolById("push#parameter2")
        if array == None or data == None:
            return CompilerException("Semantico", "Hace falta parametros en push ", self.line, self.column)
        if array.type=="any":
            array.value.append(data.value)
        elif array.type==data.type:
            array.value.append(data.value)
        else:
            return CompilerException("Semantico", "El array y el dato establecidos en los parametros no coinciden", self.line, self.column)
        return None

        