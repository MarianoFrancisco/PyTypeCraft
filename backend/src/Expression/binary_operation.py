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
        if self.operator == '+':
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


class BooleanOperator(Abstract):

    def __init__(self, l_op, r_op, op, line, column):
        self.l_op = l_op
        self.r_op = r_op
        self.op = op  # *
        self.type = 'boolean'
        super().__init__(line, column)

    def execute(self, tree, table):
        left = self.l_op.execute(tree, table)
        right = self.r_op.execute(tree, table)
        if isinstance(left, CompilerException):
            return left
        if isinstance(right, CompilerException):
            return right
        if self.op == '<':
            return left < right
        elif self.op == '>':
            return left > right
        elif self.op == '===':
            return left == right
        elif self.op == '!==':
            return left != right
        elif self.op == '<=':
            return left <= right
        elif self.op == '>=':
            return left >= right
        elif self.op == '&&':
            return left and right
        elif self.op == '||':
            return left or right
        else:
            return CompilerException("Semantico", "Operacion no valida.", self.line, self.column)
