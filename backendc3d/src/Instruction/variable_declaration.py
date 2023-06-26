from ..Semantic.c3d_generator import C3DGenerator
from ..Expression.primitive import Primitive
from ..Semantic.exception import CompilerException
from ..Abstract.abstract import Abstract
from ..Expression.identifier import Identifier,Array
from ..Semantic.symbol import Symbol
from ..Abstract.return_data import ReturnData
from typing import List

class VariableDeclaration(Abstract):

    def __init__(self, id, type, value, line, column):
        self.id = id
        self.type = type
        self.value = value
        super().__init__(line, column)
        self.search=True
        self.hide=-1
        # ASIGNANDO VALORES POR DEFECTO
        if value == None:
            if type == 'number':
                self.value = Primitive(0, 'number', self.line, self.column)
            elif type == 'boolean':
                self.value = Primitive(False, 'boolean', self.line, self.column)
            elif type == 'string':
                self.value = Primitive('', 'string', self.line, self.column)
            else:
                self.value = None
    
    def execute(self, tree, table):
        callGenerator=C3DGenerator()
        generator=callGenerator.getGenerator()
        generator.addNewComment('Variable declaration')
        
        # Verificacion de types
        if hasattr(self.value, 'id') and isinstance(self.value, Identifier):
            value = table.getSymbolById(self.value.id)
        else:
            value = self.value.execute(tree, table)
        dataType=value.type
        if isinstance(value, CompilerException): return value 
        if 'Array' in self.type and not isinstance(self.value, Array):
            return CompilerException("Semantico", f"La expresion {value} no puede asignarse a '{self.id}', ya que no es un arreglo", self.line, self.column)
        if self.type != 'any' and not ('Array' in self.type) and isinstance(self.value, Array):
            return CompilerException("Semantico", f"La variable '{self.id}' no se le puede asignar un arreglo", self.line, self.column)
        if 'any' in str(self.type) or str(dataType) in str(self.type):
            inHeap=value.getType()=='string' or value.getType()=='interface'
            symbol = table.setTable(self.id,value.type,inHeap,self.search)
        else:
            generator.addNewComment('Error: Tipo de dato es diferente al declarado')
            result = CompilerException("Semantico", "Tipo de dato es diferente al declarado", self.line, self.column)
            return result
        temporaryPosition=symbol.position
        if not symbol.isGlobal:
            temporaryPosition=generator.addNewTemporary()
            generator.addNewExpression(temporaryPosition, 'P', '+', symbol.position)
        if value.getType() == 'boolean':
            temporaryLabel = generator.addNewLabel()
            
            generator.defineLabel(value.labelTrue)
            generator.setStack(temporaryPosition, "1")
            
            generator.addGotoLabel(temporaryLabel)

            generator.defineLabel(value.labelFalse)
            generator.setStack(temporaryPosition, "0")

            generator.defineLabel(temporaryLabel)
        else:
            if isinstance(value, Symbol):
                temporary=generator.addNewTemporary()#create new temporary
                generator.getStack(temporary,value.position)
                generator.setStack(symbol.position,temporary)
            else:
                generator.setStack(temporaryPosition,value.getValue())
        generator.addNewComment('End variable declaration')
        
class ArrayDeclaration(Abstract):

    def __init__(self,id, line, column, values = None, typeAssistant = None):
        self.id = id
        self.values = values
        self.typeAssistant = typeAssistant
        self.type = 'array'
        self.size = len(values)
        self.manyDimension = False
        self.onStruct = False
        super().__init__(line, column)

    def execute(self, tree, table):
        #generator
        callGenerator=C3DGenerator()
        generator=callGenerator.getGenerator()
        if self.values:
            if isinstance(self.typeAssistant, List):#type assistant are list
                #manyDimension
                if self.type == self.typeAssistant[0]:
                    generator.addNewComment('Start array '+self.id)
                    #Add first & second temporary
                    temporaryFirst = generator.addNewTemporary()
                    temporarySecond = generator.addNewTemporary()
                    generator.addNewAssignament(temporaryFirst,'H')#new assignament, tFirst=H
                    generator.addNewExpression(temporarySecond,temporaryFirst,'+','1')#tSecond=tFirst+1
                    generator.setHeap('H', len(self.values))#heap[int(H)]=len(values)
                    pointer = str(len(self.values)+1)#pointer=values +1
                    generator.addNewExpression('H','H','+',pointer)#H=H+pointer
                    generator.addNewLine()
                    size = 0
                    #save data
                    for value in self.values:
                        if not isinstance(value, ArrayDeclaration):#not instans of array declaration
                            resultValue = value.execute(tree, table)#execute value
                            if isinstance(resultValue, CompilerException): return resultValue
                            try:#if error or not
                                if resultValue.getType() == self.typeAssistant[1]:#if result value type == type assistant
                                    generator.setHeap(temporarySecond,resultValue.getValue())#heap[int(temporarySecond)]=value of result value
                                    generator.addNewExpression(temporarySecond,temporarySecond,'+','1')#tSecond=tSecond+1
                                    generator.addNewLine()
                                    size += 1
                                else:
                                    return CompilerException("Semantico", "En el array se encuentran tipos distintos", self.line, self.column)
                            except:
                                generator.addNewComment('Error en array')
                    symbol = table.setTable(self.id,self.type,True)#set table
                    symbol.setTypeAssistant(self.typeAssistant[1])#edit data
                    symbol.setSize(size)
                    temporaryPosition=symbol.position#temporary position
                    if not symbol.isGlobal:
                        temporaryPosition=generator.addNewTemporary()
                        generator.addNewExpression(temporaryPosition, 'P','+', symbol.position)
                    generator.setStack(temporaryPosition,temporaryFirst)#stack[int(temporaryPosition)]=tFirst
                    generator.addNewComment('End array')
            else:#one dimension
                generator.addNewComment('Start array '+self.id)
                #Add first & second temporary
                temporaryFirst = generator.addNewTemporary()
                temporarySecond = generator.addNewTemporary()
                generator.addNewAssignament(temporaryFirst,'H')#new assignament, tFirst=H
                generator.addNewExpression(temporarySecond,temporaryFirst,'+','1')#tSecond=tFirst+1
                generator.setHeap('H', len(self.values))#heap[int(H)]=len(values)
                pointer = str(len(self.values)+1)#pointer=values +1
                generator.addNewExpression('H','H','+',pointer)#H=H+pointer
                generator.addNewLine()
                size = 0
                typeAssistant = []#list typeAssistant
                typeAssistant.append('array')#add array
                type = ''
                for value in self.values:
                    if not isinstance(value, ArrayDeclaration):#not instans of array declaration
                        resultValue = value.execute(tree, table)#execute value
                        if isinstance(resultValue, CompilerException): return resultValue
                        type = resultValue.getType()
                        generator.setHeap(temporarySecond,resultValue.getValue())#heap[int(temporarySecond)]=value of result value
                        generator.addNewExpression(temporarySecond,temporarySecond,'+','1')#tSecond=tSecond+1
                        generator.addNewLine()
                        size += 1
                    else:
                        value.manyDimension = True
                        value.typeAssistant = value.getType()#typeAssistant=value.type
                        resultValue = value.execute(tree, table)#execute value
                        if isinstance(resultValue, CompilerException): return resultValue
                        typeAssistant.append(resultValue.getTypeAssistant())
                        generator.setHeap(temporarySecond,resultValue.getValue())#heap[int(temporarySecond)]=value of result value
                        generator.addNewExpression(temporarySecond,temporarySecond,'+','1')#tSecond=tSecond+1
                        generator.addNewLine()
                        size += 1
                typeAssistant.append(type)#add type
                if self.manyDimension:#if many dimension
                    return ReturnData(temporaryFirst, 'array', True,0, typeAssistant)#Return adata
                if self.onStruct == False:#only if onStruct is false
                    symbol = table.setTable(self.id,self.type,True)#set table
                    symbol.setTypeAssistant(typeAssistant)#edit data
                    symbol.setSize(size)
                    temporaryPosition=symbol.position#temporary position
                    if not symbol.isGlobal:
                        temporaryPosition=generator.addNewTemporary()
                        generator.addNewExpression(temporaryPosition, 'P','+', symbol.position)
                    generator.setStack(temporaryPosition,temporaryFirst)#stack[int(temporaryPosition)]=tFirst
                    generator.addNewComment('End array')
                else:
                    return ReturnData(temporaryFirst, 'array', True,0, typeAssistant)#only return data
    '''Getter & setter'''
    def getTypeAssistant(self):
        return self.typeAssistant
    def setTypeAssistant(self, type):
        self.typeAssistant = type

    def getType(self):
        return self.type

    def getId(self):
        return self.id
    def setId(self, id):
        self.id = id
    
    def getSize(self):
        return self.size