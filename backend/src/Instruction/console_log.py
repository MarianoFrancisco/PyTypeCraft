from ..Abstract.abstract import Abstract


class ConsoleLog(Abstract):

    def __init__(self, expression, line, column):
        self.expression = expression  # <<Class.Primitivos>>
        super().__init__(line, column)

    def execute(self, tree, table):
        value = self.expression.execute(tree, table)
        tree.updateConsole(str(value))
        return None
