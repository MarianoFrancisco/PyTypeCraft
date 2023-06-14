from ..Expression.identifier import Identifier
from ..Semantic.exception import CompilerException
from ..Abstract.abstract import Abstract

class ArithmeticUnaryOperation(Abstract):
    def __init__(self, expression, operator, line, column):
        super().__init__(line, column)
        self.expression = expression
        self.operator = operator
        self.type = 'number'

    def execute(self, tree, table):
        expressionValue = self.expression.execute(tree, table)
        if isinstance(expressionValue, CompilerException):
            return expressionValue
        if self.expression.type != 'number':
            return CompilerException('Semantico', f'La expresion {expressionValue} no es un numero', self.line, self.column)
        if self.operator == '-':
            return expressionValue*(-1)
        # VERIFICAR QUE SEA UN IDENTIFICADOR Y ACTUALIZAR SU VALOR EN LA TABLA
        if self.operator == '++':
            return expressionValue+1
        if self.operator == '--':
            return expressionValue-1

class BooleanUnaryOperation(Abstract):
    def __init__(self, expression, operator, line, column):
        super().__init__(line, column)
        self.expression = expression
        self.operator = operator
        self.type = 'boolean'

    def execute(self, tree, table):
        expressionValue = self.expression.execute(tree, table)
        if isinstance(expressionValue, CompilerException):
            return expressionValue
        if self.expression.type != 'boolean':
            return CompilerException('Semantico', f'La expresion {expressionValue} no es un boolean', self.line, self.column)
        if self.operator == '!':
            return not expressionValue