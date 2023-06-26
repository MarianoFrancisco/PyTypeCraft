from ..Semantic.c3d_generator import C3DGenerator
from ..Semantic.exception import CompilerException
from ..Abstract.abstract import Abstract
from ..Abstract.return_data import ReturnData
from typing import List

class Identifier(Abstract):
    def __init__(self, id, line, column, type=None):
        self.id = id
        self.type = type
        super().__init__(line, column)

    def execute(self, tree, table):
        callGenerator=C3DGenerator()
        generator=callGenerator.getGenerator()
        generator.addNewComment('Access id'+self.id)
        symbol = table.getSymbolById(self.id)
        if symbol == None:
            generator.addNewComment('Error: End access id, variable no encontrada')
            return CompilerException("Semantico", f"Variable no encontrada {self.id}", self.line, self.column)
        temporary=generator.addNewTemporary()# save var
        temporaryPosition=symbol.position
        if not symbol.isGlobal:
            temporaryPosition=generator.addNewTemporary()
            generator.addNewExpression(temporaryPosition, 'P','+', symbol.position)
        generator.getStack(temporary,temporaryPosition)
        if (symbol.type!='boolean'):
            returnData= ReturnData(temporary,symbol.type,True)
            generator.addNewComment('End access id')
            generator.addNewLine()
            return returnData
        if self.labelTrue=='':
            self.labelTrue=generator.addNewLabel()
        if self.labelFalse=='':
            self.labelFalse=generator.addNewLabel()
        #if temporary equal one goto true else goto false
        generator.addNewIf(temporary,'1','==',self.labelTrue)
        generator.addGotoLabel(self.labelFalse)
        generator.addNewComment('End access id')
        generator.addNewLine()
        #Return the boolean
        returnData= ReturnData(temporary,'boolean',True)
        returnData.labelTrue=self.labelTrue
        returnData.labelFalse=self.labelFalse
        return returnData
        
class Array(Abstract):

    def __init__(self, id, index, line, column):
        self.id = id
        self.index = index
        super().__init__(line, column)
    
    def execute(self, tree, table):
        callGenerator=C3DGenerator()
        generator=callGenerator.getGenerator()
        generator.addNewComment('Access id '+self.id)
        variable = ''
        #if have id
        if self.id:
            variable = table.getSymbolById(self.id)#Search id
            if variable == None:
                generator.addNewComment("La variable no fue encontrada")
                return CompilerException("Semantico", "Error: La variable no fue encontrada", self.line, self.column)
        # If index out range
        generator.indexError()
        temporary = generator.addNewTemporary()#add temporary
        temporaryPosition=variable.position#temporary position
        if not variable.isGlobal:
            temporaryPosition=generator.addNewTemporary()
            generator.addNewExpression(temporaryPosition, 'P','+', variable.position)
        generator.getStack(temporary,temporaryPosition)#temporary = stack[int(temporaryPosition)]
        count = 0 
        #traversal
        type = variable.getType()
        typeAssistant = variable.getTypeAssistant()
        for valueIndex in self.index:
            count += 1
            #add first, second & third temporary
            temporaryFirst = generator.addNewTemporary()
            temporarySecond = generator.addNewTemporary()
            temporaryThird = generator.addNewTemporary()
            #add first, second & third label
            labelFirst = generator.addNewLabel()
            labelSecond = generator.addNewLabel()
            labelThird = generator.addNewLabel()
            index = valueIndex.execute(tree, table)#execute value
            if('t' in index.getValue()):
                temporaryForData=generator.addNewTemporary()
                generator.addNewExpression(temporaryForData,index.getValue(),'+',1)
                arrayDimension=temporaryForData
            else:
                arrayDimension=str(int(index.getValue())+1)
            generator.addNewExpression(temporaryFirst, temporary, "+",arrayDimension)#expression, tFirst=temporary+index.value
            generator.addNewIf(arrayDimension,'1','<',labelFirst) #if index.value<1 goto{labelFirst}, in index
            generator.getHeap(temporaryThird,temporary)#get heap, temporaryThird=heap[int(temporary)]
            generator.addNewIf(arrayDimension,temporaryThird,'>', labelFirst) #if index.value>tThird goto{labelFirst}, out index
            generator.addGotoLabel(labelSecond)#goto{labelsecond}
            generator.defineLabel(labelFirst)#lFirst:
            generator.callFunction('arrarIndexError')#call the function index error
            generator.addGotoLabel(labelThird)#goto{labelThird}
            generator.defineLabel(labelSecond)#define lSecond:
            generator.getHeap(temporarySecond, temporaryFirst)#get heap, tSecond=heap[int(tFirst)]
            generator.addGotoLabel(labelThird)#goto{lThird}
            generator.defineLabel(labelThird)#define lThird:
            temporary = temporarySecond #temporary=tSecond
            if count == len(self.index):#if count == end index
                variable.setType(variable.getTypeAssistant())#set
            else:
                if isinstance(variable.getTypeAssistant(), List):#list
                    variable.setType(variable.getTypeAssistant()[0])#position 0 type assistant
                    variable.setTypeAssistant(variable.getTypeAssistant()[1])#position 1 type assistant
                else:
                    return CompilerException("Semantico", "Error: Acceso no posible al array", self.line, self.column)
        generator.addNewComment('End access id')
        returnData = ReturnData(temporarySecond, variable.getType(), True,0, variable.getTypeAssistant())#return the data
        #set type
        variable.setType(type)
        variable.setTypeAssistant(typeAssistant)
        return returnData#return daata
    '''Get'''
    def getType(self):
        return self.type