class Symbol():

    def __init__(self, id, type, value, line, column):
        self.id = id
        self.type = type
        self.value = value
        self.line = line
        self.column = column

    def getID(self):
        return self.id

    def setID(self, id):
        self.id = id

    def getType(self):
        return self.type

    def setType(self, type):
        self.type = type

    def getValue(self):
        return self.value

    # Aqui va lo del array :3

    def setValue(self, value):
        self.value = value

    def getLine(self):
        return self.line

    def setLine(self, line):
        self.line = line

    def getColumn(self):
        return self.column

    def setColumn(self, column):
        self.column = column
