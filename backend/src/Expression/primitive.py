from ..Abstract.abstract import Abstract


class Primitive(Abstract):

    def __init__(self, type, value, line, column):
        self.type = type
        self.value = value
        super().__init__(line, column)

    def interpret(self, tree, table):
        return self.value

    def getType(self):
        return self.type
