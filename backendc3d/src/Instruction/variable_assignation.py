from ..Semantic.c3d_generator import C3DGenerator
from ..Semantic.symbol import Symbol, AnySymbol, ArraySymbol
from ..Semantic.exception import CompilerException
from ..Abstract.abstract import Abstract
from ..Expression.identifier import Identifier,Array
#from ..Expression.unary_operation import ArithmeticUnaryOperation

class VariableAssignation(Abstract):
    def __init__(self, id, value, line, column):
        super().__init__(line, column)
        self.id = id
        self.value = value

    def execute(self, tree, table):
        callGenerator=C3DGenerator()
        generator=callGenerator.getGenerator()
        generator.addNewComment('Modify variable')
        symbol = table.getSymbolById(self.id)

        if hasattr(self.value, 'expression') and isinstance(self.value.expression, Identifier):
            valueResult=table.getSymbolById(self.value.expression.id)
        else:
            valueResult=self.value.execute(tree, table)
        if symbol == None:
            generator.addNewComment('Error: End modify variable, variable no encontrada')
            return CompilerException("Semantico", f"Variable no encontrada {self.id}", self.line, self.column)
        if isinstance(symbol, CompilerException): return symbol
        if isinstance(self.value,Identifier):
            if not isinstance(symbol, AnySymbol) and valueResult.type != symbol.type:
                return CompilerException('Semantico', f'El valor {valueResult} no coincide con el tipo {symbol.type} de la variable {self.id}', self.line, self.column)
        else:
            if not isinstance(symbol, AnySymbol) and self.value.type != symbol.type:
                return CompilerException('Semantico', f'El valor {valueResult} no coincide con el tipo {symbol.type} de la variable {self.id}', self.line, self.column)
        if isinstance(symbol, ArraySymbol) and not isinstance(self.value, Array):
            return CompilerException("Semantico", f"La expresion {valueResult} no puede asignarse a '{self.id}', ya que no es un arreglo", self.line, self.column)
        if not isinstance(symbol, AnySymbol) and not isinstance(symbol, ArraySymbol) and isinstance(self.value, Array):
            return CompilerException("Semantico", f"La variable '{self.id}' no se le puede asignar un arreglo", self.line, self.column)
        if isinstance(symbol, AnySymbol) and isinstance(self.value, Array):
            symbol.type = f'Array<{self.value.type}>'
        if isinstance(valueResult, Symbol):
            temporary=generator.addNewTemporary()#create new temporary
            if(self.value.operator=='-'):
                    generator.getStack(temporary,valueResult.position)
                    temporary2=generator.addNewTemporary()#add temporary, 0 to invert the sign
                    generator.addNewExpression(temporary2, '0', self.value.operator, temporary)
                    generator.setStack(symbol.position,temporary2)
            else:
                generator.getStack(temporary,valueResult.position)
                generator.setStack(symbol.position,temporary)
        else:
            generator.setStack(symbol.position,valueResult.getValue())
        return None