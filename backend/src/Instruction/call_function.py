from ..Abstract.abstract import Abstract
from ..Semantic.exception import CompilerException
from ..Semantic.symbol import Symbol
from ..Semantic.symbol_table import SymbolTable_

class CallFunction(Abstract):

    def __init__(self, name,parameters,line,column):
        self.name = name
        self.parameters = parameters
        super().__init__(line,column)
    
    def execute(self, tree,table):
        function = tree.getFunction(self.name)
        if function == None:
            return CompilerException("Semantico", "No se encontro la funcion: " + str(self.name), str(self.line), str(self.column))
        entorn = SymbolTable_(tree.getGlobalScope())
        #print(str(self.parameters))
        if len(self.parameters) == len(function.parameters):
            count = 0
            for expression in self.parameters:
                
                result_expression = expression.execute(tree, table)
                
                if isinstance(result_expression, CompilerException): return result_expression
                
                if function.parameters[count]['type'] == expression.type:
                    symbol = Symbol(str(function.parameters[count]['id']), expression.type, result_expression, self.line, self.column)
                    
                    result = entorn.setTableFunction(symbol)
                    if isinstance(result, CompilerException): return result
                else:
                    return CompilerException("Semantico", "Tipo de dato diferente en Parametros", str(self.line), str(self.column))
                count += 1
        
        value = function.execute(tree, entorn) # me puede retornar un valor
        if isinstance(value, CompilerException): return value
        self.type = function.type
        return value
