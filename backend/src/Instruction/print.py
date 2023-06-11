from ..Abstract.abstract import Abstract


class Print(Abstract):

    def __init__(self, expression, line, column):
        self.expression = expression  # <<Class.Primitivos>>
        super().__init__(line, column)

    def interpret(self, tree, table):
        value = self.expression.interpret(tree, table)
        print(value)
        tree.updateConsole(str(value))
        return value
