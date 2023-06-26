from ..Abstract.abstract import Abstract


class Null(Abstract):

    def __init__(self, line, column):
        super().__init__(line, column)
        self.type = 'any'

    def execute(self, tree, table):
        return None
    
