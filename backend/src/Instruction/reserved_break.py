
from ..Abstract.abstract import Abstract
import uuid

class ReservedBreak(Abstract):

    def __init__(self, line, column):
        self.line = line
        self.colum = column
    
    def execute(self, tree, table):
        return self
    
    def plot(self, root):
        node_id = str(uuid.uuid4())
        root.node(node_id, "Break")
        return node_id