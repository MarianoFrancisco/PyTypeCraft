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
            return ReturnData(temporary,self.type, True)
        else:
                return CompilerException("Semantico", "Operacion no valida.", self.line, self.column)


class BooleanOperation(Abstract):

    def __init__(self, l_op, r_op, operator, line, column):
        self.l_op = l_op
        self.r_op = r_op
        self.operator = operator  # *
        self.type = 'boolean'
        super().__init__(line, column)

    def execute(self, tree, table):
        callGenerator=C3DGenerator()
        generator=callGenerator.getGenerator()
        temporary=''
        left = self.l_op.execute(tree, table)
        right = self.r_op.execute(tree, table)
        if isinstance(left, CompilerException):
            return left
        if isinstance(right, CompilerException):
            return right
        op=self.operator
        if(op=='<' or op=='>' or op=='===' or op=='!==' or op=='<=' or op=='>=' or op=='||'):
            temporary=generator.addNewTemporary()
            generator.addNewExpression(temporary,left.value,op,right.value)
            return ReturnData(temporary,self.type, True)
        else:
            return CompilerException("Semantico", "Operacion no valida.", self.line, self.column)