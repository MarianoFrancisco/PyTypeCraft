from ..Abstract.abstract import Abstract
from ..Semantic.exception import CompilerException

class Struct(Abstract):
    def __init__(self, id, data, line, column):
        super().__init__(line, column)
        self.id = id
        self.data = data

    def execute(self, tree, table):
        dataMod={}
        for attribute in self.data:
            if tree.getInterfaceById(attribute["type"]) == None:
                return CompilerException("Semantico", f"La interfaz {attribute['type']} no está declarada", self.line, self.column)
            dataMod[attribute["id"]] = attribute["type"]
        self.data = dataMod

