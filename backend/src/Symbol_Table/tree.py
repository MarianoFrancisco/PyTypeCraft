class Tree:

    def __init__(self, instructions):
        self.instructions = instructions
        self.functions = []
        self.exceptions = []
        self.console = ""
        self.globalScope = None
        self.interpretedGlobalScope = {}

    # Hacer los getters y setters de cada atributo

    def setInterpretedGlobalScope(self, scope, value):
        self.interpretedGlobalScope[scope] = value

    def getInterpretedGlobalScope(self):
        return self.interpretedGlobalScope  # devolvemos el entorno global

    def getInstr(self):
        return self.instructions

    def setInstr(self, instructions):
        self.instructions = instructions

    def getFunctions(self):
        return self.functions

    def setFunctions(self, functions):
        self.functions.append(functions)

    def getFunction(self, ide):
        for funcion in self.functions:
            if funcion.ide == ide:
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
