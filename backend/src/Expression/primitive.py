from ..Abstract.abstract import Abstract


class Primitive(Abstract):

    def __init__(self, value, type, line, column):
        super().__init__(line, column)
        self.value = value
        self.type = type

    def execute(self, tree, table):
        return self.value
    
