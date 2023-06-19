from ..Semantic.exception import CompilerException
from ..Semantic.symbol import Symbol
from ..Semantic.symbol import Symbol, ArraySymbol, AnySymbol
from ..Expression.array import Array

class SymbolTable:

    def __init__(self, prevScope=None):
        self.table = {}  # Al inicio la table esta vacia
        self.prevScope = prevScope  # Apuntador al entorno prevScope
        '''New data'''
        self.labelBreak=''
        self.labelReturn=''
        self.labelContinue=''
        self.retainTemporaries=False
        self.size=0#Pointer
        if prevScope!=None:
            self.size=self.prevScope.size

    def getGlobalScope(self):
        return self.table

    def addSymbol(self, symbol):
        # Aqui va la verificacion de que no se declare una variable dos veces
        self.table[symbol.id] = symbol

    def setTableFunction(self, symbol):
        self.table[symbol.id] = symbol

    def setTable(self,id,type,inHeap,search=True):
        if search:
            currentTable=self
            while currentTable != None:
                if id in currentTable.table:
                    currentTable.table[id].setType(type)
                    currentTable.table[id].setInHeap(inHeap)
                    return currentTable.table[id]
                else:
                    currentTable=currentTable.prevScope
        if id in self.table:
            self.table[id].setType(type)
            self.table[id].setInHeap(inHeap)
            return self.table[id]
        else:
            # if 'any' in type:
            #     symbol=Symbol(id,type,self.size,inHeap,self.prevScope==None)
            #     if isinstance(value, Array):
            #         symbol.type = f'Array<{type}>'  
            # elif isinstance(value, Array):
            #     symbol = ArraySymbol(id,type,self.size,inHeap,self.prevScope==None)
            # else:
            #     symbol=Symbol(id,type,self.size,inHeap,self.prevScope==None)
            symbol=Symbol(id,type,self.size,inHeap,self.prevScope==None)
            self.size+=1# add new var, move stack
            self.table[id]=symbol
            return self.table[id]

    def getSymbolById(self, id):  # Se obtiene el entorno
        currentScope = self
        while currentScope != None:
            if id in currentScope.table:
                return currentScope.table[id]
            else:
                currentScope = currentScope.prevScope
        return None

    def updateSymbol(self, symbol):
        currentScope = self
        while currentScope != None:
            if symbol.id in currentScope.table:
                currentScope.table[symbol.id].value = symbol.value
                currentScope.table[symbol.id].type = symbol.type
                return None
                # Si necesitan cambiar el tipo de dato
                # currentScope.table[symbol.id].setTipo(symbol.getTipo())
            else:
                currentScope = currentScope.prevScope
        return CompilerException("Semantico", f"Variable {id} no encontrada.", symbol.line, symbol.column)
