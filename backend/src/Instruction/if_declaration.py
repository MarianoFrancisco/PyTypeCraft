from ..Semantic.exception import CompilerException
from ..Semantic.symbol_table import SymbolTable
from ..Abstract.abstract import Abstract

class IfSentence(Abstract):

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
            scope = SymbolTable(table)  #NUEVO ENTORNO - HIJO - Vacio
            for instruccion in self.ifBlock:
                result = instruccion.execute(tree, scope) 
                if isinstance(result, CompilerException) :
                    tree.setExceptions(result)
        elif self.elseBlock != None:
            scope = SymbolTable(table)
            for instruccion in self.elseBlock:
                result = instruccion.execute(tree, scope) 
                if isinstance(result, CompilerException) :
                    tree.setExceptions(result)
        elif self.elseIfBlock != None:
            result = self.elseIfBlock.execute(tree, table)
