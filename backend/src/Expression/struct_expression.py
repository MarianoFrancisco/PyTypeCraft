from ..Semantic.exception import CompilerException
from ..Abstract.abstract import Abstract


class StructExpression(Abstract):
    def __init__(self, attributes, line, column):
        super().__init__(line, column)
        self.attributes = attributes
        # POSIBLEMENTE IMPLEMENTAR TIPOS
        self.type = 'any'

    def execute(self, tree, table):
        data = {}
        for attribute in self.attributes:
            result = attribute["value"].execute(tree, table)
            if isinstance(result, CompilerException): return result
            data[attribute["id"]] = result
        return data