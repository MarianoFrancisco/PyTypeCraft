from abc import ABC, abstractmethod


class AbstractSymbol(ABC):

    def __init__(self, id, type, value, line, column):
        self.id = id
        self.type = type
        self.value = value
        self.line = line
        self.column = column

    @abstractmethod
    def getValue(self): pass

    @abstractmethod
    def setValue(self): pass

    @abstractmethod
    def getType(self): pass


class Symbol(AbstractSymbol):

    def __init__(self, id, type, value, line, column):
        super().__init__(id, type, value, line, column)

    # PENDIENTE CREAR LOGICA PARA VALORES DE ARREGLOS
    def getValue(self):
        return self.value

    def setValue(self, value):
        self.value = value

    def getType(self):
        return self.type


class AnySymbol(Symbol):

    def __init__(self, id, type, value, line, column):
        super().__init__(id, type, value, line, column)
