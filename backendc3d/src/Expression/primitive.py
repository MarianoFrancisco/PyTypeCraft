from ..Abstract.abstract import Abstract
from ..Abstract.return_data import ReturnData
from ..Semantic.c3d_generator import C3DGenerator

class Primitive(Abstract):

    def __init__(self, value, type, line, column):
        super().__init__(line, column)
        self.value = value
        self.type = type

    def execute(self, tree, table):
        callGenerator=C3DGenerator()
        generator=callGenerator.getGenerator()
        return ReturnData(str(self.value),self.type,False)
        #return self.value
    
    def getType(self):
        return self.type
