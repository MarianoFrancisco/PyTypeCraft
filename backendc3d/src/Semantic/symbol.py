from abc import ABC, abstractmethod


class AbstractSymbol(ABC):

    def __init__(self, id, type, position, inHeap,isGlobal):
        self.id = id
        self.type = type
        self.position = position
        self.inHeap=inHeap
        self.isGlobal=isGlobal
        self.value=None
        self.typeAssistant=''#for array
        self.size=0#size of data
        self.reference=False
        self.parameters=None
    
    '''Getter & setters'''
    @abstractmethod
    def getId(self): pass
    @abstractmethod
    def setId(self): pass

    @abstractmethod
    def getType(self): pass
    @abstractmethod
    def setType(self): pass

    @abstractmethod
    def getPosition(self): pass
    @abstractmethod
    def setPosition(self): pass

    @abstractmethod
    def getInHeap(self): pass
    @abstractmethod
    def setInHeap(self): pass
    
    @abstractmethod
    def getValue(self): pass
    @abstractmethod
    def setValue(self): pass

    @abstractmethod
    def getTypeAssistant(self): pass
    @abstractmethod
    def setTypeAssistant(self): pass

    @abstractmethod
    def getSize(self): pass
    @abstractmethod
    def setSize(self): pass

    @abstractmethod
    def getReference(self): pass
    @abstractmethod
    def setReference(self): pass

    @abstractmethod
    def getParameters(self): pass
    @abstractmethod
    def setParameters(self): pass
    


class Symbol(AbstractSymbol):
    # type puede ser solo number, string, boolean
    def __init__(self, id, type, position, inHeap,isGlobal):
        super().__init__(id, type, position, inHeap,isGlobal)
    
    def getId(self):
        return self.id
    
    def setId(self,id):
        self.id = id

    def getType(self):
        return self.type
    
    def setType(self,type):
        self.type = type

    def getPosition(self):
        return self.position
    
    def setPosition(self,position):
        self.position = position

    def getInHeap(self):
        return self.inHeap
    
    def setInHeap(self,inHeap):
        self.inHeap = inHeap
    
    def getValue(self):
        return self.value
    
    def setValue(self,value):
        self.value = value
    
    def getTypeAssistant(self):
        return self.typeAssistant

    def setTypeAssistant(self,typeAssistant):
        self.typeAssistant = typeAssistant
    
    def getSize(self):
        return self.size
    
    def setSize(self,size):
        self.size = size
    
    def getReference(self):
        return self.reference
    
    def setReference(self,reference):
        self.reference = reference

    def getParameters(self):
        return self.parameters
    
    def setParameters(self,parameters):
        self.parameters = parameters

# clase para identificar a los simbolos que son arreglos
class ArraySymbol(AbstractSymbol):
    # type puede ser solo number, string, boolean
    def __init__(self, id, type, position, inHeap,isGlobal):
        super().__init__(id, type, position, inHeap,isGlobal)

    # PENDIENTE CREAR LOGICA PARA VALORES DE ARREGLOS
    def getId(self):
        return self.id
    
    def setId(self,id):
        self.id = id

    def getType(self):
        return self.type
    
    def setType(self,type):
        self.type = type

    def getPosition(self):
        return self.position
    
    def setPosition(self,position):
        self.position = position

    def getInHeap(self):
        return self.inHeap
    
    def setInHeap(self,inHeap):
        self.inHeap = inHeap
    
    def getValue(self):
        return self.value
    
    def setValue(self,value):
        self.value = value
    
    def getTypeAssistant(self):
        return self.typeAssistant

    def setTypeAssistant(self,typeAssistant):
        self.typeAssistant = typeAssistant
    
    def getSize(self):
        return self.size
    
    def setSize(self,size):
        self.size = size
    
    def getReference(self):
        return self.reference
    
    def setReference(self,reference):
        self.reference = reference

    def getParameters(self):
        return self.parameters
    
    def setParameters(self,parameters):
        self.parameters = parameters
    
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
    def __init__(self, id, type, position, inHeap,isGlobal):
        super().__init__(id, type, position, inHeap,isGlobal)

    def getId(self):
        return self.id
    
    def setId(self,id):
        self.id = id

    def getType(self):
        return self.type
    
    def setType(self,type):
        self.type = type

    def getPosition(self):
        return self.position
    
    def setPosition(self,position):
        self.position = position

    def getInHeap(self):
        return self.inHeap
    
    def setInHeap(self,inHeap):
        self.inHeap = inHeap
    
    def getValue(self):
        return self.value
    
    def setValue(self,value):
        self.value = value
    
    def getTypeAssistant(self):
        return self.typeAssistant

    def setTypeAssistant(self,typeAssistant):
        self.typeAssistant = typeAssistant
    
    def getSize(self):
        return self.size
    
    def setSize(self,size):
        self.size = size
    
    def getReference(self):
        return self.reference
    
    def setReference(self,reference):
        self.reference = reference

    def getParameters(self):
        return self.parameters
    
    def setParameters(self,parameters):
        self.parameters = parameters