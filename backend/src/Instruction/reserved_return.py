from ..Abstract.abstract import Abstract
from ..Semantic.exception import CompilerException

class ReservedReturn(Abstract):

    def __init__(self,expression, line,column):
        self.expression = expression
        self.value = None
        self.type = None
        super().__init__(line,column)
    
    def execute(self, tree,table):
        return_result = self.expression.execute(tree, table)
        if isinstance(return_result, CompilerException): return return_result
        self.type = self.expression.type
        self.value = return_result
        return self