from ..Semantic.symbol_table import SymbolTable_
from ..Abstract.abstract import Abstract

class If_sentence(Abstract):

    def __init__(self, condition, ifBlock, elseBlock, elseIfBlock, line, column):
        self.condition = condition
        self.ifBlock = ifBlock
        self.elseBlock = elseBlock
        self.elseIfBlock = elseIfBlock
        super().__init__(line, column)
    

    def execute(self, tree, table):
        condition = self.condition.execute(tree, table)
        if isinstance(condition, Exception): return condition
        # Validar que el tipo sea booleano
        if bool(condition) == True:
            scope = SymbolTable_(table)  #NUEVO ENTORNO - HIJO - Vacio
            for instruccion in self.ifBlock:
                result = instruccion.execute(tree, scope) 
                if isinstance(result, Exception) :
                    tree.setExceptiones(result)
        elif self.elseBlock != None:
            scope = SymbolTable_(table)
            for instruccion in self.elseBlock:
                result = instruccion.execute(tree, scope) 
                if isinstance(result, Exception) :
                    tree.setException(result)
        elif self.elseIfBlock != None:
            result = self.elseIfBlock.execute(tree, table)
