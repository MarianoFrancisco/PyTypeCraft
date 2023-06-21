from ..Semantic.exception import CompilerException
from ..Abstract.abstract import Abstract
from ..Abstract.return_data import ReturnData
from ..Semantic.c3d_generator import C3DGenerator

class ArithmeticOperation(Abstract):
    # en el nivel mas bajo se espera que se reciban privitivo + primitivo
    def __init__(self, l_op, r_op, operator, line, column):
        self.l_op = l_op  # <<Class.Primitivos>>
        self.r_op = r_op  # <<Class.Primitivos>>
        self.operator = operator  # *
        self.type = "number"
        super().__init__(line, column)

    # PENDIENTE DE REALIZAR LA VERIFICACION DE TIPOS
    def execute(self, tree, table):
        callGenerator=C3DGenerator()
        generator=callGenerator.getGenerator()
        generator.addNewComment('Start expression aritmetic')
        temporary=''
        left_value = self.l_op.execute(tree, table)
        right_value = self.r_op.execute(tree, table)
        if isinstance(left_value, CompilerException):
            return left_value.value
        if isinstance(right_value, CompilerException):
            return right_value.value
        if left_value.type != right_value.type:
            return CompilerException('Semantico', 'Los valores a operar no coinciden', self.line, self.column)
        # if self.l_op.type != 'number' or self.r_op.type != 'number':
        #     return CompilerException('Semantico', 'Los valores a operar no son numericos', self.line, self.column)
        # op=self.operator
        op=self.operator
        if(op=='+' or op=='-' or op=='*' or op=='/' or op=='%' or op=='^'):
            temporary=generator.addNewTemporary()
            generator.addNewExpression(temporary,left_value.value,op,right_value.value)
            if left_value.type == 'string':
                if op=='+':
                    self.type = 'string'
                else:
                    generator.addNewComment('Error: se intenta operar string y no es suma')
            elif left_value.type == 'number':
                self.type='number'
            else:
                generator.addNewComment('Error: Los tipos no coinciden')
            generator.addNewComment('End expression aritmetic')
            return ReturnData(temporary,self.type, True)
        else:
                return CompilerException("Semantico", "Operacion no valida.", self.line, self.column)


class RelationalOperation(Abstract):

    def __init__(self, l_op, r_op, operator, line, column):
        self.l_op = l_op
        self.r_op = r_op
        self.operator = operator  # *
        self.type = 'boolean'
        super().__init__(line, column)

    def execute(self, tree, table):
        callGenerator=C3DGenerator()
        generator=callGenerator.getGenerator()
        generator.addNewComment('Start expression relational')
        left = self.l_op.execute(tree, table)
        if isinstance(left, CompilerException):
            return left
        right = None
        returnData=ReturnData(None,'boolean',False)
        if (left.type!='boolean'):
            right=self.r_op.execute(tree, table)
            if isinstance(right, CompilerException):
                return right
            if left.type =='number' and right.type=='number':#comparate type
                self.comprobateLabel()# if exist label add, else create
                generator.addNewIf(left.value,right.value,self.operator,self.labelTrue)
                generator.addGotoLabel(self.getLabelFalse())

            elif left.type =='string' and right.type=='string':#comparate type
                if self.operator=='===' or self.operator=='!==':#Only you can contrast string with TREQ & NOTEQDB
                    generator.contrastString()
                    temporaryParameter=generator.addNewTemporary()#Create one parameter temporary
                    #left, obtain stack and set to obtain expression
                    generator.addNewExpression(temporaryParameter, 'P','+',table.size)#define and add 1
                    generator.addNewExpression(temporaryParameter, temporaryParameter,'+',1)
                    #add stack
                    generator.setStack(temporaryParameter,right.getValue())
                    #right, obtain stack and set to obtain expression
                    generator.addNewExpression(temporaryParameter, temporaryParameter,'+',1)
                    #add stack
                    generator.setStack(temporaryParameter,left.getValue())
                    generator.newEnvironment(table.size)
                    generator.callFunction('contrastString')
                    temporary=generator.addNewTemporary()#add new temporary
                    generator.getStack(temporary, 'P')
                    generator.returnEnvironment(table.size)#Join and leave into environment
                    self.comprobateLabel()#comprobate label
                    generator.addNewIf(temporary,self.getBinaryType(),"==",self.labelTrue)
                    generator.addGotoLabel(self.labelFalse)
                    generator.addNewComment('End expression relational')
                    generator.addNewLine()
                    returnData.labelTrue=self.labelTrue
                    returnData.labelFalse=self.labelFalse
                    return returnData
        generator.addNewComment('End expression relational')
        generator.addNewLine()
        returnData.labelTrue=self.labelTrue
        returnData.labelFalse=self.labelFalse
        return returnData
    # Comprobate the label
    def comprobateLabel(self):
        callGenerator=C3DGenerator()
        generator=callGenerator.getGenerator()
        if self.labelTrue=='':
            self.labelTrue=generator.addNewLabel()
        if self.labelFalse=='':
            self.labelFalse=generator.addNewLabel()
    #Obtain 1 for == and 0 for !==, 1 equal, 0 distinct
    def getBinaryType(self):
        if self.operator == '===':
            return '1'
        if self.operator == '!==':
            return '0'
class LogicOperation(Abstract):

    def __init__(self, l_op, r_op, operator, line, column):
        self.l_op = l_op
        self.r_op = r_op
        self.operator = operator  # *
        self.type = 'boolean'
        super().__init__(line, column)

    def execute(self, tree, table):
        callGenerator=C3DGenerator()
        generator=callGenerator.getGenerator()
        generator.addNewComment('Start expression logic')
        
        