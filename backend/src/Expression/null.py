from ..Abstract.abstract import Abstract
import uuid

class Null(Abstract):

    def __init__(self, line, column):
        super().__init__(line, column)
        self.type = 'any'

    def execute(self, tree, table):
        return None
    
    def plot(self, root):
        id = str(uuid.uuid4())
        root.node(id, 'null')
        return id
    
