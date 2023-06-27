from ..Semantic.exception import CompilerException
from ..Abstract.abstract import Abstract
import uuid

class StructExpression(Abstract):
    def __init__(self, attributes, line, column):
        super().__init__(line, column)
        self.attributes = attributes
        # POSIBLEMENTE IMPLEMENTAR TIPOS
        self.type = 'any'

    def execute(self, tree, table):
        data = {}
        for attribute in self.attributes:
            result = attribute["value"].execute(tree, table)
            if isinstance(result, CompilerException): return result
            data[attribute["id"]] = result
        return data
    
    def plot(self, root):
        id = str(uuid.uuid4())

        # Generar los nodos para cada atributo
        for attribute in self.attributes:
            inner_id = str(uuid.uuid4())
            root.node(inner_id, attribute["id"])
            root.edge(id, inner_id)
            root.edge(inner_id, attribute["value"].plot(root))

        # Generar el nodo final para la expresión de tipo struct
        root.node(id, '{}')

        return id
