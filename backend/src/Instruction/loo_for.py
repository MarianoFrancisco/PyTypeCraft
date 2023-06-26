from ..Instruction.reserved_break import ReservedBreak
from ..Instruction.reserved_continue import ReservedContinue
from ..Instruction.reserved_return import ReservedReturn
from ..Expression.primitive import Primitive
from ..Instruction.variable_assignation import VariableAssignation
from ..Semantic.symbol import Symbol
from ..Semantic.exception import CompilerException
from ..Abstract.abstract import Abstract
from ..Semantic.symbol_table import SymbolTable

class For(Abstract):

    def __init__(self, declaration, restriction, variation, instruction, line,column):
        self.declaration = declaration
        self.restriction = restriction
        self.variation = variation
        self.instruction = instruction
        super().__init__(line,column)
    
    def execute(self, tree, table):
        entorn = SymbolTable(table)
        declaration = self.declaration.execute(tree, entorn)
        if isinstance(declaration, CompilerException): return declaration

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
                    return result
                if isinstance(result, ReservedReturn): return result
                if isinstance(result, ReservedBreak): return None
                if isinstance(result, ReservedContinue): break
            variation = self.variation.execute(tree, entorn)
            if isinstance(variation, CompilerException): return variation
            # symbol = Symbol(self.declaration.id, self.declaration.type, variation, self.line, self.column)
            # # Actualizando el valor de la variable en la tabla de simbolos
            # value = entorn.updateSymbol(symbol)

            # if isinstance(value, CompilerException): return value
            
            # primitive = Primitive(variation, self.declaration.type, self.declaration.line, self.declaration.column)
            # result = VariableAssignation(self.declaration.id, primitive, primitive.line, primitive.column).execute(tree, entorn)
            # if isinstance(result, CompilerException): return result
            restriction = self.restriction.execute(tree, entorn)
            if isinstance(restriction, CompilerException):
                tree.setExceptions(restriction)
                return restriction
            if self.restriction.type != 'boolean':
                return CompilerException("Semantico", "Tipo de dato no booleano en FOR.", self.line, self.column)
        return None
            


class ForOf(Abstract):

    def __init__(self, declaration, array, instructions, line,column):
        self.declaration = declaration
        self.array = array
        self.instructions = instructions
        super().__init__(line,column)
    
    def execute(self, tree, table):
        entorn = SymbolTable(table)
        localVariable = self.declaration.execute(tree, entorn)
        if isinstance(localVariable, CompilerException): return localVariable

        arr = self.array.execute(tree, entorn)
        if isinstance(arr, CompilerException): return arr

        if not isinstance(arr, str) and not isinstance(arr, list):
            return CompilerException("Semantico", f"El valor no es un iterable", self.line, self.column)
        
        for i in range(len(arr)):
            primitive = Primitive(arr[i], self.array.type, self.array.line, self.array.column)
            result = VariableAssignation(self.declaration.id, primitive, primitive.line, primitive.column).execute(tree, entorn)
            if isinstance(result, CompilerException): return result
            for instruction in self.instructions:
                resultInstruction = instruction.execute(tree, entorn)
                if isinstance(resultInstruction, CompilerException):
                    tree.setExceptions(result)
                    return resultInstruction
                if isinstance(resultInstruction, ReservedReturn): return resultInstruction
                if isinstance(resultInstruction, ReservedBreak): return None
                if isinstance(resultInstruction, ReservedContinue): break
        return None