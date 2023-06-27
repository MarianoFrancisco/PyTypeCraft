class CompilerException:

    def __init__(self, type, desc, line, column):
        self.type = type
        self.desc = desc
        self.line = line
        self.column = column

    def __str__(self) -> str:
        return 'ERROR ' + self.type + ' - ' + self.desc + ' [' + str(self.line) + ', ' + str(self.column) + '];'
    def toString(self):
        return self.type + ' - ' + self.desc + ' [' + str(self.line) + ', ' + str(self.column) + '];'
    def toStringData(self):
        stringData = str(self.type) +" ,"+str(self.desc) +" ," + str(self.line)+" ," +str(self.column)
        return stringData