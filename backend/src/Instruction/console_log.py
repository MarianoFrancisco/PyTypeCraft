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
        first_element_id = self.params[0].plot(root)
        prevId = id
        for param in self.params[1:]:
            inner_id = str(uuid.uuid4())
            root.node(inner_id, ',')
            root.edge(prevId, inner_id)
            root.edge(inner_id, param.plot(root))
            prevId = inner_id
        root.node(id, "console.log")
        root.edge(id, first_element_id)
        return id
