from ..Semantic.exception import CompilerException
from ..Abstract.abstract import Abstract

class ArithmeticOperation(Abstract):
    # en el nivel mas bajo se espera que se reciban privitivo + primitivo
    def __init__(self, l_op, r_op, operator, line, column):
        self.l_op = l_op  # <<Class.Primitivos>>
        self.r_op = r_op  # <<Class.Primitivos>>
        self.operator = operator  # *
        self.type = 'number'
        super().__init__(line, column)

    # PENDIENTE DE REALIZAR LA VERIFICACION DE TIPOS
    def execute(self, tree, table):
        left_value = self.l_op.execute(tree, table)
        right_value = self.r_op.execute(tree, table)
        if isinstance(left_value, CompilerException):
            return left_value
        if isinstance(right_value, CompilerException):
            return right_value
        if self.l_op.type != self.r_op.type:
            return CompilerException('Semantico', 'Los valores a operar no coinciden', self.line, self.column)
        if self.operator == '+':
            if self.l_op.type == 'string':
                self.type = 'string'
            return left_value + right_value
        if self.l_op.type != 'number' or self.r_op.type != 'number':
            return CompilerException('Semantico', 'Los valores a operar no son numericos', self.line, self.column)
        if self.operator == '-':
            return left_value - right_value
        elif self.operator == '*':
            return left_value * right_value
        elif self.operator == '/':
            return left_value / right_value
        elif self.operator == '%':
            return left_value % right_value
        elif self.operator == '^':
            return left_value ** right_value


class BooleanOperation(Abstract):

    def __init__(self, l_op, r_op, operator, line, column):
        self.l_op = l_op
        self.r_op = r_op
        self.operator = operator  # *
        self.type = 'boolean'
        super().__init__(line, column)

    def execute(self, tree, table):
        left = self.l_op.execute(tree, table)
        right = self.r_op.execute(tree, table)
        if isinstance(left, CompilerException):
            return left
        if isinstance(right, CompilerException):
            return right
        
        # # VERIFICANDO QUE LOS OPERANDOS COINCIDAN EN TIPOS
        # if self.l_op.type != self.r_op.type:
        #     return CompilerException('Semantico', 'Los tipos de los operandos no coinciden', self.line, self.column)
        # # VERIFICANDO LAS OPERACIONES QUE PUEDEN REALIZAR STRINGS Y NUMBERS
        # if self.operator in ['>', '<', '>=', '<=']:
        #     if self.l_op.type != 'number' or self.l_op.type != 'string':
        #         return CompilerException('Semantico', f'No se puede realizar la operacion {self.operator} para {self.l_op.type}')
        # else:
        #     if self.l_op.type != 'boolean':
        #         return CompilerException('Semantico', f'No se puede realizar la operacion {self.operator} para {self.l_op.type}')  
        if self.operator == '<':  
            return left < right
        elif self.operator == '>':
            return left > right
        elif self.operator == '===':
            return left == right
        elif self.operator == '!==':
            return left != right
        elif self.operator == '<=':
            return left <= right
        elif self.operator == '>=':
            return left >= right
        elif self.operator == '&&':
            return left and right
        elif self.operator == '||':
            return left or right
        else:
            return CompilerException("Semantico", "Operacion no valida.", self.line, self.column)
