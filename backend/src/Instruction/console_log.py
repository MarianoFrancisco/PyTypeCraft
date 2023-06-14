from ..Abstract.abstract import Abstract


class ConsoleLog(Abstract):

    def __init__(self, params, line, column):
        self.params = params  # <<Class.Primitivos>>
        super().__init__(line, column)

    def execute(self, tree, table):
        result = ''
        for param in self.params:
            value = param.execute(tree, table)
            result += str(value) + ' '
        tree.updateConsole(result.strip())
        return None
