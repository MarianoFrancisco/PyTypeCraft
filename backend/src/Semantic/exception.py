class CompilerException:

    def __init__(self, type, desc, line, column):
        self.type = type
        self.desc = desc
        self.line = line
        self.column = column

    def toString(self):
        return self.type + ' - ' + self.desc + ' [' + str(self.line) + ', ' + str(self.column) + '];'
