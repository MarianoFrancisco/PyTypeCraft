class Tree_:
    
    def __init__(self, instructions):
        self.instructions = instructions
        self.functions = []
        self.exceptions = []
        self.interfaces = {}
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

    def getFunction(self, id):
        for function in self.functions:
            if function.name == id:
                return function
        return None
    
    def addInterface(self, interface):
        self.interfaces[interface.id] = interface

    def getInterfaceById(self, id):
        return self.interfaces.get(id)
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
    
