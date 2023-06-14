class Tree_:
    
    def __init__(self, instructions):
        self.instructions = instructions
        self.functions = []
        self.exceptions = []
        self.console = ""
        self.globalScope = None
        self.globalScopeExecuted = {}
    
    # Hacer los getters y setters de cada atributo

    def setGlobalScopeExecuted(self, entorno, valor):
        self.globalScopeExecuted[entorno] = valor
    
    def getGlobalScopeExecuted(self):
        return self.globalScopeExecuted # devolvemos el entorno global

    def getInstr(self):
        return self.instructions

    def setInstr(self, instructions):
        self.instructions = instructions
    
    def getFunctions(self):
        return self.functions
    
    def setFunctions(self, functions):
        self.functions.append(functions)

    def getFuncion(self, id):
        for funcion in self.functions:
            if funcion.id == id:
                return funcion
        return None
    
    def getExceptions(self):
        return self.exceptions
    
    def setExceptions(self, exceptions):
        self.exceptions.append(exceptions)
    
    def getConsole(self):
        return self.console
    
    def setConsole(self, console):
        self.console = console
    
    def updateConsole(self, console):
        self.console += console + '\n'
    
    def getGlobalScope(self):
        return self.globalScope

    def setGlobalScope(self, globalScope):
        self.globalScope = globalScope
    
