from ..Abstract.abstract import Abstract
from ..Semantic.c3d_generator import C3DGenerator
from ..Semantic.exception import CompilerException

class ConsoleLog(Abstract):

    def __init__(self, params, line, column):
        self.params = params  # <<Class.Primitivos>>
        super().__init__(line, column)

    def execute(self, tree, table):
        callGenerator=C3DGenerator()
        generator=callGenerator.getGenerator()
        #value = self.params.execute(tree, table)
        result = ''
        for param in self.params:
            value = param.execute(tree, table)
            result += str(value) + ' ' 
            if isinstance(value,CompilerException):return value
            if value.getType()=="number":
                generator.addConsoleLog('f',value.getValue())
            elif value.getType()=="string":
                generator.addConsoleLog('s',f'"{value.getValue()}"')
            elif value.getType()=="boolean":
                generator.addConsoleLog('t',value.getValue().lower())
        tree.updateConsole(result.strip())
        return None
