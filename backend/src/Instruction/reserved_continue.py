
from ..Abstract.abstract import Abstract

class ReservedContinue(Abstract):

    def __init__(self, line, column):
        self.line = line
        self.colum = column
    
    def execute(self, tree, table):
        return self