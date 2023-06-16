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
    # type puede ser solo number, string, boolean
    def __init__(self, id, type, value, line, column):
        super().__init__(id, type, value, line, column)

    # PENDIENTE CREAR LOGICA PARA VALORES DE ARREGLOS
    def getValue(self):
        return self.value

    def setValue(self, value):
        self.value = value

    def getType(self):
        return self.type

# clase para identificar a los simbolos que son arreglos
class ArraySymbol(AbstractSymbol):
    # type puede ser solo number, string, boolean
    def __init__(self, id, type, value, line, column):
        super().__init__(id, type, value, line, column)

    # PENDIENTE CREAR LOGICA PARA VALORES DE ARREGLOS
    def getValue(self):
        return self.value

    def setValue(self, value):
        self.value = value

    def getType(self):
        return self.type
    
    def getValue(arr, indices):
        try:
            for index in indices:
                arr = arr[index]
        except (IndexError, TypeError):
            return None
        else:
            return arr


class AnySymbol(AbstractSymbol):
    # value es una instancia de Symbol o ArraySymbol. En any no puede ponerse un struct
    def __init__(self, id, type, value, line, column):
        super().__init__(id, type, value, line, column)

    def getValue(self):
        return self.value

    def setValue(self, value):
        self.value = value

    def getType(self):
        return self.type
