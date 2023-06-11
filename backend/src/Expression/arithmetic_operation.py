from ..Abstract.abstract import Abstract


class ArithmeticOperation(Abstract):

    def __init__(self, l_op, r_op, op, line, column):
        self.l_op = l_op  # <<Class.Primitivos>>
        self.r_op = r_op  # <<Class.Primitivos>>
        self.op = op  # *
        self.type = None
        super().__init__(line, column)

    def interpret(self, tree, table):
        left = self.l_op.interpret(tree, table)
        right = self.r_op.interpret(tree, table)
        if self.op == '+':
            if left.type == 'number' and right.type == 'number':
                return left + right
            elif left.type == 'string' and right.type == 'string':
                return left + right
            elif left.type == 'string' and right.type == 'number':
                return 'Error: No se puede sumar un string con un number'
            elif left.type == 'number' and right.type == 'string':
                return 'Error: No se puede sumar un number con un string'
            else:
                return 'Error: Tipo de dato invalido en suma'
        elif self.op == '-':
            return left - right
        elif self.op == '*':
            return left * right
        elif self.op == '/':
            if right == 0:
                return 'Error: Division entre 0'
            return left / right
