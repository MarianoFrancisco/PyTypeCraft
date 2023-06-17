from ..Abstract.abstract import Abstract
from ..Semantic.c3d_generator import C3DGenerator

class ConsoleLog(Abstract):

    def __init__(self, params, line, column):
        self.params = params  # <<Class.Primitivos>>
        super().__init__(line, column)

    def execute(self, tree, table):
        callGenerator=C3DGenerator()
        generator=callGenerator.getGenerator()
        result = ''
        for param in self.params:
            value = param.execute(tree, table)
            result += str(value) + ' '
        tree.updateConsole(result.strip())
        return None
