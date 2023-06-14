from ..Semantic.exception import CompilerException
from ..Semantic.symbol_table import SymbolTable_
from ..Abstract.abstract import Abstract
from ..Instruction.reserved_return import ReservedReturn

class If_sentence(Abstract):

    def __init__(self, condition, ifBlock, elseBlock, elseIfBlock, line, column):
        super().__init__(line, column)
        self.condition = condition
        self.ifBlock = ifBlock
        self.elseBlock = elseBlock
        self.elseIfBlock = elseIfBlock
    

    def execute(self, tree, table):
        conditionEvaluated = self.condition.execute(tree, table)
        if isinstance(conditionEvaluated, CompilerException): return conditionEvaluated
        # Validar que el tipo sea booleano
        if bool(conditionEvaluated) == True:
            scope = SymbolTable_(table)  #NUEVO ENTORNO - HIJO - Vacio
            for instruccion in self.ifBlock:
                result = instruccion.execute(tree, scope) 
                if isinstance(result, CompilerException) :
                    tree.setExceptions(result)
                if isinstance(result, ReservedReturn): return result
        elif self.elseBlock != None:
            scope = SymbolTable_(table)
            for instruccion in self.elseBlock:
                result = instruccion.execute(tree, scope) 
                if isinstance(result, CompilerException) :
                    tree.setExceptions(result)
                if isinstance(result, ReservedReturn): return result
        elif self.elseIfBlock != None:
            result = self.elseIfBlock.execute(tree, table)
            if isinstance(result, ReservedReturn): return result
