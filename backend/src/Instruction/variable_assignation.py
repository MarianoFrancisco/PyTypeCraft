from ..Expression.array import Array
from ..Semantic.symbol import Symbol, AnySymbol, ArraySymbol
from ..Semantic.exception import CompilerException
from ..Abstract.abstract import Abstract
import uuid

class VariableAssignation(Abstract):
    def __init__(self, id, value, line, column):
        super().__init__(line, column)
        self.id = id
        self.value = value

    def execute(self, tree, table):
        valueResult = self.value.execute(tree, table)
        if isinstance(valueResult, CompilerException): return valueResult
        symbol = table.getSymbolById(self.id)
        if isinstance(symbol, CompilerException): return symbol
        if not isinstance(symbol, AnySymbol) and self.value.type != symbol.type:
            return CompilerException('Semantico', f'El valor {valueResult} no coincide con el tipo {symbol.type} de la variable {self.id}', self.line, self.column)
        
        if isinstance(symbol, ArraySymbol) and not isinstance(self.value, Array):
            return CompilerException("Semantico", f"La expresion {valueResult} no puede asignarse a '{self.id}', ya que no es un arreglo", self.line, self.column)
        if not isinstance(symbol, AnySymbol) and not isinstance(symbol, ArraySymbol) and isinstance(self.value, Array):
            return CompilerException("Semantico", f"La variable '{self.id}' no se le puede asignar un arreglo", self.line, self.column)
        symbolUpdated = Symbol(self.id, self.value.type, valueResult, self.line, self.column)
        
        if isinstance(symbol, AnySymbol) and isinstance(self.value, Array):
            symbol.type = f'Array<{self.value.type}>'
        result = table.updateSymbol(symbolUpdated)
        if isinstance(result, CompilerException):
            return result
        return None
    
    def plot(self, root):
        node_id = str(uuid.uuid4())
        root.node(node_id, "Variable Assignation")
        id_node_id = str(uuid.uuid4())
        root.node(id_node_id, self.id)
        # Create nodes for id and value
        value_node_id = self.value.plot(root)

        # Create edge from the root node to id and value nodes
        root.edge(node_id, id_node_id)
        root.edge(node_id, value_node_id)

        return node_id
    
# DEFINIR BIEN LA ASIGNACION DE VARIABLES
class VariableArrayAssignation(VariableAssignation):
    def __init__(self, id, value, indexes, line, column):
        super().__init__(id, value, line, column)
        self.indexes = indexes

    def execute(self, tree, table):
        valueResult = self.value.execute(tree, table)
        if isinstance(valueResult, CompilerException): return valueResult
        symbol = table.getSymbolById(self.id)
        if symbol == None:
            return CompilerException("Semantico", f"Variable no encontrada {self.id}", self.line, self.column)
        # if not isinstance(symbol, ArraySymbol)
        indexes = []
        for index in self.indexes:
            indexResult = index.execute(tree, table)
            if isinstance(indexResult, CompilerException): return indexResult
            if index.type != 'number':
                return CompilerException("Semantico", f"El valor {indexResult} no es un indice numerico valido para acceder al arreglo", index.line, index.column)
            indexes.append(indexResult)

        result = self.setValueArrayIndex(symbol.value, indexes, valueResult)
        if isinstance(result, CompilerException): return result
        return None
    
    def setValueArrayIndex(self, arr, indexes, val):
        try:
            target = arr
            for index in indexes[:-1]:
                target = target[index]
            target[indexes[-1]] = val
        except (IndexError, TypeError):
            return CompilerException("Semantico", "Indice fuera de rango", self.line, self.column)
        else: return None

class VariableStructAssignation(VariableAssignation):
    def __init__(self, id, keys, value, line, column):
        super().__init__(id, value, line, column)
        self.keys = keys

    def execute(self, tree, table):
        valueResult = self.value.execute(tree, table)
        if isinstance(valueResult, CompilerException): return valueResult
        symbol = table.getSymbolById(self.id)
        if symbol == None:
            return CompilerException("Semantico", f"Variable no encontrada {self.id}", self.line, self.column)
        result = self.setAttributeStruct(symbol.value, self.keys, valueResult)
        if isinstance(result, CompilerException): return result
        return None
        
    def setAttributeStruct(self, dictionary, keys, value):
        try:
            last_key = keys[-1]
            nested_dict = dictionary
            for key in keys[:-1]:
                nested_dict = nested_dict[key]
            nested_dict[last_key] = value
        except (KeyError, TypeError):
            return CompilerException("Semantico", f"No existe ese atributo en el struct {self.id}", self.line, self.column)
        else: return None
