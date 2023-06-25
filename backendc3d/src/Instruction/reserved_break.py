from ..Abstract.abstract import Abstract

class ReservedBreak(Abstract):

    def __init__(self, line, column):
        super().__init__(line, column)
        
    def execute(self, tree, table):
        return self