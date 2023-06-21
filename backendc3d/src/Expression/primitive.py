from ..Abstract.abstract import Abstract
from ..Abstract.return_data import ReturnData
from ..Semantic.c3d_generator import C3DGenerator

class Primitive(Abstract):

    def __init__(self, value, type, line, column):
        super().__init__(line, column)
        self.value = value
        self.type = type#typeAssistant

    def execute(self, tree, table):
        callGenerator=C3DGenerator()
        generator=callGenerator.getGenerator()
        if self.type=='number':
            return ReturnData(str(self.value),self.type,False)
        elif self.type=='string':
            temporary = generator.addNewTemporary()
            generator.addNewAssignament(temporary, 'H')#Heap
            for char in  str(self.value):
                generator.setHeap('H',ord(char))
                generator.nextHeap()#position heap
            generator.setHeap('H',-1)#End Heap
            generator.nextHeap()#position heap
            return ReturnData(temporary,self.type,True)#for heap true
        elif self.type == 'boolean':#create new label for true and false
            if self.labelTrue=='':
                generator.addNewLabel()
            if self.labelFalse=='':
                generator.addNewLabel()
            if self.value:#if value first true, else false first, but if not is the instruction execute the other gotolabel
                generator.addGotoLabel(self.labelTrue)
                generator.addGotoLabel(self.labelFalse)
            else:
                generator.addGotoLabel(self.labelFalse)
                generator.addGotoLabel(self.labelTrue)
            returnData=ReturnData(self.value,self.type,False)#False because aren't temporary
            #change data for true & false label
            returnData.labelTrue=self.labelTrue
            returnData.labelFalse=self.labelFalse
            return returnData
    
    def getType(self):
        return self.type
