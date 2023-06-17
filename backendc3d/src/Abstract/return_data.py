class ReturnData:
    ''' For go to, when we can't leave set parameters, if is a list use typeAssistant, size plus-minus to heap and stack for pointers'''
    def __init__(self, value, type, isTemporary, size=0, typeAssistant= "", reference= ''):
        self.value = value
        self.type = type
        self.isTemporary = isTemporary
        self.size = size
        self.typeAssistant = typeAssistant
        self.reference = reference
        self.labelTrue = ''
        self.labelFalse = ''
    ''' Getter & setter value, type, typeAssistant, reference, size, label true & false'''
    def getValue(self):
        return self.value
    def setValue(self, value):
        self.value = value

    def getType(self):
        return self.type
    def setType(self, type):
        self.type = type

    def getSize(self):
        return self.size
    def setLength(self, size):
        self.size= size

    def getTypeAssistant(self):
        return self.typeAssistant
    def setTypeAssistant(self, typeAssistant):
        self.typeAssistant = typeAssistant

    def getReference(self):
        return self.reference
    def setReference(self, reference):
        self.reference = reference

    def getLabelTrue(self):
        return self.labelTrue
    def setTrueLbl(self, labelTrue):
        self.labelTrue = labelTrue

    def getLabelFlase(self):
        return self.labelFalse
    def setFalseLbl(self, labelFalse):
        self.labelFalse = labelFalse
    
    
    
    
    
    