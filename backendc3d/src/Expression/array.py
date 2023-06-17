from ..Semantic.exception import CompilerException
from ..Abstract.abstract import Abstract


class Array(Abstract):
    def __init__(self, expressions, line, column):
        super().__init__(line, column)
        self.expressions = expressions
        self.type = None

    def execute(self, tree, table):
        arr = []
        for value in self.expressions:
            result = value.execute(tree, table)
            if isinstance(result, CompilerException): return result
            if self.type != None and self.type != value.type:
                self.type = 'any'
            else:
                self.type = value.type
            arr.append(result)
        return arr
