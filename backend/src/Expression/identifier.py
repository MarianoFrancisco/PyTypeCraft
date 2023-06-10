from ..Table_Simbolos.excepcion import Excepcion
from ..Abstract.abstract import Abstract


class Identificador(Abstract):
    def __init__(self, id, line, column, type=None):
        self.id = id
        self.line = line
        self.column = column
        self.type = type

    def interpretar(self, tree, table):
        simbolo = table.getTable(self.id)
        if simbolo == None:
            return Excepcion("Semantico", "Variable no encontrada", self.line, self.column)
        self.type = simbolo.getType()
        return simbolo.getValor()

    def getType(self):
        return self.type

    def getID(self):
        return self.id
