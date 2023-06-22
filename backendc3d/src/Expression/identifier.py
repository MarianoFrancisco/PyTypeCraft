from ..Semantic.c3d_generator import C3DGenerator
from ..Semantic.exception import CompilerException
from ..Abstract.abstract import Abstract
from ..Abstract.return_data import ReturnData

class Identifier(Abstract):
    def __init__(self, id, line, column, type=None):
        self.id = id
        self.line = line
        self.column = column
        self.type = type

    def execute(self, tree, table):
        callGenerator=C3DGenerator()
        generator=callGenerator.getGenerator()
        generator.addNewComment('Access id')
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
        
        