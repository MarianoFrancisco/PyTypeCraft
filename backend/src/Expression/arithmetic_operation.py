from ..Abstract.abstract import Abstract


class Aritmetica(Abstract):

    def __init__(self, l_op, r_op, op, line, column):
        self.l_op = l_op  # <<Class.Primitivos>>
        self.r_op = r_op  # <<Class.Primitivos>>
        self.op = op  # *
        super().__init__(line, column)

    def interpret(self, tree, table):
        left = self.l_op.interpret(tree, table)
        l_type = self.l_op.getTipo()
        right = self.r_op.interpret(tree, table)
        r_type = self.r_op.getTipo()
        if self.op == '+':
            if l_type == 'number' and r_type == 'number':
                return left + right
            elif l_type == 'string' and r_type == 'string':
                return left + right
            elif l_type == 'string' and r_type == 'number':
                return 'Error: No se puede sumar un string con un number'
            elif l_type == 'number' and r_type == 'string':
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
