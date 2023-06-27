from ..Abstract.abstract import Abstract
import uuid

class Primitive(Abstract):

    def __init__(self, value, type, line, column):
        super().__init__(line, column)
        self.value = value
        self.type = type

    def execute(self, tree, table):
        return self.value
    
    def getType(self):
        return self.type

    def plot(self, root):
        id = str(uuid.uuid4())
        root.node(id, str(self.value))
        return id