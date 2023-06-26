from ..Abstract.abstract import Abstract


class Struct(Abstract):
    def __init__(self, id, data, line, column):
        super().__init__(line, column)
        self.id = id
        self.data = data

    def execute(self, tree, table):
        pass

