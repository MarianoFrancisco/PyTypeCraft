from ..Expression.primitive import Primitive
from ..Instruction.variable_assignation import VariableAssignation
from ..Expression.identifier import Identifier
from ..Semantic.exception import CompilerException
from ..Abstract.abstract import Abstract
import uuid

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
        # EN ESTE PUNTO YA SE ASUME QUE SE TRABAJA CON UNA INSTANCIA DE IDENTIFIER DEBIDO A LA GRAMATICA
        if not isinstance(self.expression, Identifier):
            return CompilerException('Semantico', f'El operador ++ y -- solo funcionan con variables declaradas', self.line, self.column)
        if self.operator == '++':
            primitive = Primitive(expressionValue+1, 'number', self.line, self.column)
            result = VariableAssignation(self.expression.id, primitive, self.line, self.column).execute(tree, table)
            if isinstance(result, CompilerException): return result
            return expressionValue+1
        if self.operator == '--':
            primitive = Primitive(expressionValue-1, 'number', self.line, self.column)
            result = VariableAssignation(self.expression.id, primitive, self.line, self.column).execute(tree, table)
            if isinstance(result, CompilerException): return result
            return expressionValue-1
        
    def plot(self, root):
        id = str(uuid.uuid4())
        root.node(id, self.operator)
        left_id = self.expression.plot(root)
        root.edge(id, left_id)
        return id

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
        
    def plot(self, root):
        id = str(uuid.uuid4())
        root.node(id, self.operator)
        left_id = self.expression.plot(root)
        root.edge(id, left_id)
        return id