from ..Instruction.reserved_return import ReservedReturn
from ..Abstract.abstract import Abstract
from ..Semantic.exception import CompilerException
from ..Semantic.symbol_table import SymbolTable

class Function(Abstract):

    def __init__(self, name, parameters, instructions, line,column):
        self.name = name
        self.parameters = parameters
        self.instructions = instructions
        self.type = 'number'
        super().__init__(line,column)
    

    def execute(self, tree,table):
        entorn = SymbolTable(table)
        for instruction in self.instructions:
            function = instruction.execute(tree, entorn)
            if isinstance(function, CompilerException): return function
            if isinstance(function, ReservedReturn):
                self.type = function.type
                return function.value
        return None