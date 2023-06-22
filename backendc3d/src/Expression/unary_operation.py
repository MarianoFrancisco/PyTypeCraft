from ..Semantic.symbol import Symbol
from ..Semantic.c3d_generator import C3DGenerator
from ..Expression.primitive import Primitive
from ..Instruction.variable_assignation import VariableAssignation
from ..Expression.identifier import Identifier
from ..Semantic.exception import CompilerException
from ..Abstract.abstract import Abstract
from ..Abstract.return_data import ReturnData

class ArithmeticUnaryOperation(Abstract):
    def __init__(self, expression, operator, line, column):
        super().__init__(line, column)
        self.expression = expression
        self.operator = operator
        self.type = 'number'

    def execute(self, tree, table):
        ##call generator
        callGenerator=C3DGenerator()
        generator=callGenerator.getGenerator()
        generator.addNewComment('Start unary operation')
        if isinstance(self.expression,Identifier):
            expressionValue=table.getSymbolById(self.expression.id)
        else:
            expressionValue = self.expression.execute(tree, table)
            if self.expression.type != 'number':
                return CompilerException('Semantico', f'La expresion {expressionValue} no es un numero', self.line, self.column)
        if isinstance(expressionValue, CompilerException):
            return expressionValue
        if isinstance(expressionValue, Symbol):
            temporary=generator.addNewTemporary()#create new temporary t0
            if(self.operator=='-'):
                generator.getStack(temporary,expressionValue.position)#t0=stack[int(num)]
                temporary2=generator.addNewTemporary()#add temporary, 0 to invert the sign t1
                generator.addNewExpression(temporary2, '0', self.operator, temporary)#t1=0-t0
                return ReturnData(temporary2, self.type, True)
            elif(self.operator=='++'):
                generator.getStack(temporary,expressionValue.position)
                temporary2=generator.addNewTemporary()#add temporary, 0 to invert the sign
                generator.addNewExpression(temporary2, '1', '+', temporary)
                generator.setStack(expressionValue.position,temporary2)
                return ReturnData(temporary, self.type, True)
            elif(self.operator=='--'):
                generator.getStack(temporary,expressionValue.position)
                temporary2=generator.addNewTemporary()#add temporary, 0 to invert the sign
                generator.addNewExpression(temporary2, '-1', '+', temporary)
                generator.setStack(expressionValue.position,temporary2)
                return ReturnData(temporary, self.type, True)
        else:
            if self.operator == '-':
                temporary=generator.addNewTemporary()#add temporary, 0 to invert the sign
                generator.addNewExpression(temporary, '0', self.operator, expressionValue.getValue())
                return ReturnData(temporary, self.type, True)
            else:
                return CompilerException('Semantico', f'El operador - solo funciona con number', self.line, self.column)
        generator.addNewComment('End unary operation')

class BooleanUnaryOperation(Abstract):
    def __init__(self, expression, operator, line, column):
        super().__init__(line, column)
        self.expression = expression
        self.operator = operator
        self.type = 'boolean'

    def execute(self, tree, table):
        ##call generator
        callGenerator=C3DGenerator()
        generator=callGenerator.getGenerator()
        generator.addNewComment('Start unary logic')
        self.comprobateLabel()
        if self.operator == '!':
            self.expression.setLabelFalse(self.labelTrue) 
            self.expression.setLabelTrue(self.labelFalse)
            labelNot = self.expression.execute(tree, table)
            if isinstance(labelNot, CompilerException): return labelNot
            if labelNot.getType() != 'boolean':
                return CompilerException("Semantico", "No se puede usar expresion boolean en: ", self.fila, self.column)
            labelTrue = labelNot.getLabelTrue()
            labelFalse = labelNot.getLabelFalse()
            labelNot.setLabelTrue(labelFalse)
            labelNot.setLabelFalse(labelTrue)
            return labelNot
        expressionValue = self.expression.execute(tree, table)
        if isinstance(expressionValue, CompilerException):
            return expressionValue
        if expressionValue.getType() != 'boolean':
            return CompilerException('Semantico', f'La expresion {expressionValue} no es un boolean', self.line, self.column)
        if self.operator == '!':
            return not expressionValue
        generator.addNewComment('End unary logic')
        generator.addNewLine()
        returnData = ReturnData(None, 'boolean', False)
        returnData.setLabelTrue(self.labelTrue)
        returnData.setLabelFalse(self.labelFalse)
        return returnData
    # Comprobate the label
    # Comprobate the label
    def comprobateLabel(self):
        callGenerator=C3DGenerator()
        generator=callGenerator.getGenerator()
        if self.labelTrue=='':
            self.labelTrue=generator.addNewLabel()
        if self.labelFalse=='':
            self.labelFalse=generator.addNewLabel()