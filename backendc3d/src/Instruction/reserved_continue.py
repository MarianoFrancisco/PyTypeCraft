from ..Abstract.abstract import Abstract

class ReservedContinue(Abstract):

    def __init__(self, line, column):
        super().__init__(line, column)
    
    def execute(self, tree, table):
        return self