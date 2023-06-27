from ..Expression.identifier import Identifier
from ..Semantic.symbol import Symbol
from ..Semantic.exception import CompilerException
from ..Abstract.abstract import Abstract
import uuid

class Array(Abstract):
    def __init__(self, expressions, line, column):
        super().__init__(line, column)
        self.expressions = expressions
        self.type = None

    def execute(self, tree, table):
        arr = []
        for value in self.expressions:
            result = value.execute(tree, table)
            if isinstance(result, CompilerException): return result
            # if self.type != None and self.type != value.type or isinstance(value, Array):
            if self.type != None and self.type != value.type:
                self.type = 'any'
            else:
                self.type = value.type
            # if self.type != None and isinstance(value, Array):
            #     self.type = f"{self.type}"
            arr.append(result)
        return arr
    
    def plot(self, root):
        id = str(uuid.uuid4())

        # Generar el nodo para el primer elemento
        first_element_id = self.expressions[0].plot(root)
        prevId = id
        # Generar los nodos para los elementos restantes
        for expression in self.expressions[1:]:
            inner_id = str(uuid.uuid4())
            root.node(inner_id, ',')
            root.edge(prevId, inner_id)
            root.edge(inner_id, expression.plot(root))
            prevId = inner_id

        # Generar el nodo final para la expresión de tipo array
        root.node(id, '[]')
        root.edge(id, first_element_id)

        return id