from ..Symbol_Table.exception import CompilerException
from ..Abstract.abstract import Abstract


class Relacional_Logica(Abstract):

    def __init__(self, l_op, r_op, op, line, column):
        self.l_op = l_op
        self.r_op = r_op
        self.op = op  # *
        self.type = 'boolean'
        super().__init__(line, column)

    def interpret(self, tree, table):
        left = self.l_op.interpret(tree, table)
        if isinstance(left, CompilerException):
            return left
        if self.op != '!':
            right = self.r_op.interpret(tree, table)
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
        elif self.op == '!':
            return not left
        else:
            return CompilerException("Semantico", "Operacion no valida.", self.line, self.column)

    def getType(self):
        return self.type

    def getValue(self, type, val):
        # aqui hacen validacion del type de dato
        return str(val)
