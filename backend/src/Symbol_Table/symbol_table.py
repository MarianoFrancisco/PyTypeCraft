from ..Symbol_Table.exception import CompilerException


class SymbolTable:

    def __init__(self, prevScope=None):
        self.table = {}  # Al inicio la table esta vacia
        self.prevScope = prevScope  # Apuntador al entorno prevScope

    def getGlobalTable(self):
        return self.table

    def setTable(self, simbolo):
        # Aqui va la verificacion de que no se declare una variable dos veces
        self.table[simbolo.getID()] = simbolo

    def setTableFuncion(self, simbolo):
        self.table[simbolo.getID()] = simbolo

    def getTable(self, ide):  # Aqui manejamos los entornos :3
        tableActual = self
        while tableActual != None:
            if ide in tableActual.table:
                return tableActual.table[ide]
            else:
                tableActual = tableActual.prevScope
        return None

    def updateTable(self, simbolo):
        tableActual = self
        while tableActual != None:
            if simbolo.getID() in tableActual.table:
                tableActual.table[simbolo.getID()].setValor(simbolo.getValue())
                return None
                # Si necesitan cambiar el tipo de dato
                # tableActual.table[simbolo.getID()].setTipo(simbolo.getTipo())
            else:
                tableActual = tableActual.prevScope
        return CompilerException("Semantico", "Variable no encontrada.", simbolo.getLine(), simbolo.getColumn())
