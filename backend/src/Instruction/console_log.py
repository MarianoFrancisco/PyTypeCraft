from ..Abstract.abstract import Abstract
import uuid

class ConsoleLog(Abstract):

    def __init__(self, params, line, column):
        self.params = params  # <<Class.Primitivos>>
        super().__init__(line, column)

    def execute(self, tree, table):
        result = ''
        for param in self.params:
            value = param.execute(tree, table)
            result += str(value) + ' '
        tree.updateConsole(result.strip())
        return None
    
    def plot(self, root):
        id = str(uuid.uuid4())
        root.node(id, "console.log")
        for param in self.params:
            param_id = param.plot(root)
            root.edge(id, param_id)
        return id
