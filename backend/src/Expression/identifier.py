from ..Semantic.exception import CompilerException
from ..Abstract.abstract import Abstract
import uuid


class Identifier(Abstract):
    def __init__(self, id, line, column, type=None):
        self.id = id
        self.line = line
        self.column = column
        self.type = type

    def execute(self, tree, table):
        symbol = table.getSymbolById(self.id)
        if symbol == None:
            return CompilerException("Semantico", f"Variable no encontrada {self.id}", self.line, self.column)
        self.type = symbol.type
        return symbol.value
    
    def plot(self, root):
        id = str(uuid.uuid4())
        root.node(id, str(self.id))
        return id

# llamando valores que sean de un array a traves de sus indices PENDIENTE DE IMPLEMENTAR
class IdentifierArray(Abstract):
    def __init__(self, id, indexes, line, column, type=None):
        self.id = id
        self.line = line
        self.column = column
        self.indexes = indexes
        self.type = type

    def execute(self, tree, table):
        symbol = table.getSymbolById(self.id)
        if symbol == None:
            return CompilerException("Semantico", f"Variable no encontrada {self.id}", self.line, self.column)
        self.type = symbol.type
        arr = symbol.value
        # if not isinstance(symbol, ArraySymbol)

        try:
            for index in self.indexes:
                result = index.execute(tree, table)
                if isinstance(result, CompilerException): return result
                arr = arr[result]
        except (IndexError, TypeError):
            return CompilerException("Semantico", f"Indice fuera de rango", self.line, self.column)
        else:
            return arr

    def plot(self, root):
        id = str(uuid.uuid4())
        first_element_id = str(uuid.uuid4())
        root.node(first_element_id, self.id)
        prevId = id
        for index in self.indexes:
            inner_id = str(uuid.uuid4())
            root.node(inner_id, '[ ]=')
            root.edge(prevId, inner_id)
            root.edge(inner_id, index.plot(root))
            prevId = inner_id

        root.node(id, '[ ]=')
        root.edge(id, first_element_id)
        return id

    
class IdentifierStruct(Abstract):
    def __init__(self, id, keys, line, column):
        super().__init__(line, column)
        self.id = id
        self.keys = keys

    def execute(self, tree, table):
        symbol = table.getSymbolById(self.id)
        if symbol == None:
            return CompilerException("Semantico", f"Variable no encontrada {self.id}", self.line, self.column)
        value = symbol.value
        try:
            for key in self.keys:
                value = value[key]
        except (KeyError, TypeError):
            return CompilerException("Semantico", f"El struct no contiene el atributo {key}", self.line, self.column)
        else:
            return value
        
    def plot(self, root):
        id = str(uuid.uuid4())
        first_element_id = str(uuid.uuid4())
        root.node(first_element_id, self.id)
        prevId = id
        for key in self.keys:
            inner_id = str(uuid.uuid4())
            root.node(inner_id, '.')
            root.edge(prevId, inner_id)
            root.edge(inner_id, key)
            prevId = inner_id

        root.node(id, '.')
        root.edge(id, first_element_id)
        return id