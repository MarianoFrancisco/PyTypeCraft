from ..Semantic.exception import CompilerException


class SymbolTable:

    def __init__(self, prevScope=None):
        self.table = {}  # Al inicio la table esta vacia
        self.prevScope = prevScope  # Apuntador al entorno prevScope

    def getGlobalScope(self):
        return self.table

    def addSymbol(self, symbol):
        # Aqui va la verificacion de que no se declare una variable dos veces
        self.table[symbol.id] = symbol

    def setTableFunction(self, symbol):
        self.table[symbol.id] = symbol

    def getSymbolById(self, id):  # Se obtiene el entorno
        currentScope = self
        while currentScope != None:
            if id in currentScope.table:
                return currentScope.table[id]
            else:
                currentScope = currentScope.prevScope
        return None

    def updateSymbol(self, symbol):
        currentScope = self
        while currentScope != None:
            if symbol.id in currentScope.table:
                currentScope.table[symbol.id].value = symbol.value
                return None
                # Si necesitan cambiar el tipo de dato
                # currentScope.table[symbol.id].setTipo(symbol.getTipo())
            else:
                currentScope = currentScope.prevScope
        return CompilerException("Semantico", f"Variable {id} no encontrada.", symbol.line, symbol.column)
