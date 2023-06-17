from ..Semantic.symbol import Symbol
from ..Semantic.exception import CompilerException
from ..Abstract.abstract import Abstract
from ..Semantic.symbol_table import SymbolTable

class For(Abstract):

    def __init__(self, requirement, restriction, variation, instruction, line,column):
        self.requirement = requirement
        self.restriction = restriction
        self.variation = variation
        self.instruction = instruction
        super().__init__(line,column)
    
    def execute(self, tree, table):
        entorn = SymbolTable(table)
        requirement = self.requirement.execute(tree, entorn)
        if isinstance(requirement, CompilerException): return requirement

        restriction = self.restriction.execute(tree, entorn)
        if isinstance(restriction, CompilerException): return restriction
        # Validar que el tipo sea booleano
        if self.restriction.type != 'boolean':
            return CompilerException("Semantico", "Tipo de dato no booleano en FOR.", self.line, self.column)
        # Recorriendo las instrucciones
        while restriction:
            for instruction in self.instruction:
                result = instruction.execute(tree, entorn)
                if isinstance(result, CompilerException):
                    tree.exceptions.append(result)
            variation = self.variation.execute(tree, entorn)
            if isinstance(variation, CompilerException): return variation
            symbol = Symbol(self.requirement.id, self.requirement.type, variation, self.line, self.column)
            # Actualizando el valor de la variable en la tabla de simbolos
            value = entorn.updateSymbol(symbol)

            if isinstance(value, CompilerException): return value

            restriction = self.restriction.execute(tree, entorn)
            if isinstance(restriction, CompilerException): return restriction
            if self.restriction.type != 'boolean':
                return CompilerException("Semantico", "Tipo de dato no booleano en FOR.", self.line, self.column)
        return None
            


