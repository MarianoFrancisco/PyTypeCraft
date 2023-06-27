import uuid
from ..Abstract.abstract import Abstract

class ReservedContinue(Abstract):

    def __init__(self, line, column):
        self.line = line
        self.colum = column
    
    def execute(self, tree, table):
        return self
    
    def plot(self, root):
        node_id = str(uuid.uuid4())
        root.node(node_id, "Continue")
        return node_id