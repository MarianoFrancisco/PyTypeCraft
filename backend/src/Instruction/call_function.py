from ..Abstract.abstract import Abstract
from ..Semantic.exception import CompilerException
from ..Semantic.symbol import Symbol
from ..Semantic.symbol_table import SymbolTable

class CallFunction(Abstract):

    def __init__(self, name,parameters,line,column):
        self.name = name
        self.parameters = parameters
        super().__init__(line,column)
    
    def execute(self, tree,table):
        function = tree.getFunction(self.name)
        if function == None:
            return CompilerException("Semantico", "No se encontro la funcion: " + str(self.name), str(self.line), str(self.column))
        entorn = SymbolTable(tree.getGlobalScope())
        if len(self.parameters) == len(function.parameters):
            count = 0
            for expression in self.parameters:
                
                result_expression = expression.execute(tree, table)
                
                if isinstance(result_expression, CompilerException): return result_expression
                
                if function.parameters[count]['type'] == expression.type:
                    symbol = Symbol(str(function.parameters[count]['id']), expression.type, result_expression, self.line, self.column)
                    result = entorn.setTableFunction(symbol)
                    if isinstance(result, CompilerException): return result
                elif function.parameters[count]['type']=='any':
                    symbol = Symbol(str(function.parameters[count]['id']), expression.type, result_expression, self.line, self.column)
                    result = entorn.setTableFunction(symbol)
                    if isinstance(result, CompilerException): return result
                elif function.parameters[count]["type"]=="NoType":
                    symbol = Symbol(str(function.parameters[count]['id']), expression.type, result_expression, self.line, self.column)
                    result = entorn.setTableFunction(symbol)
                    if isinstance(result, CompilerException): return result
                else:
                    if(self.name=="toLowerCase"):
                        return CompilerException("Semantico", "La funcion nativa toLowerCase unicamente acepta string como parametro", str(-1), str(-1))
                    elif(self.name=="length"):
                        return CompilerException("Semantico", "La funcion nativa length unicamente acepta string o array como parametro", str(-1), str(-1))
                    elif(self.name=="toExponential"):
                        return CompilerException("Semantico", "La funcion nativa toExponential unicamente acepta string como parametros", str(-1), str(-1))
                    elif(self.name=="toUpperCase"):
                        return CompilerException("Semantico", "La funcion nativa toUpperCase unicamente acepta string como parametro", str(-1), str(-1))
                    elif(self.name=="toFixed"):
                        return CompilerException("Semantico", "La funcion nativa toFixed unicamente acepta number como parametros", str(-1), str(-1))
                    else:
                        return CompilerException("Semantico", "Tipo de dato diferente en Parametros en la funcion "+self.name, str(self.line), str(self.column))
                count += 1
        
        value = function.execute(tree, entorn) # me puede retornar un valor
        if isinstance(value, CompilerException): return value
        self.type = function.type
        return value
