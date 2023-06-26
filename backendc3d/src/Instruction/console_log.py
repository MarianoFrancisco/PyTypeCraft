from ..Abstract.abstract import Abstract
from ..Semantic.c3d_generator import C3DGenerator
from ..Semantic.exception import CompilerException
from typing import List

class ConsoleLog(Abstract):

    def __init__(self, params, line, column):
        self.params = params  # <<Class.Primitivos>>
        super().__init__(line, column)

    def execute(self, tree, table):
        callGenerator=C3DGenerator()
        generator=callGenerator.getGenerator()
        for param in self.params:
            value = param.execute(tree, table)
            if isinstance(value,CompilerException):return value
            if isinstance(value.type,List):
                if('number' in value.type):
                    value.type='number'
                elif('string' in value.type):
                    value.type='string'
                elif('boolean' in value.type):
                    value.type='boolean'
            if value.getType()=="number":
                generator.addConsoleLog('f',value.getValue())
            elif value.getType()=="string":
                generator.consoleString()
                temporaryParameter=generator.addNewTemporary()
                generator.addNewExpression(temporaryParameter,'P','+',table.size)
                generator.addNewExpression(temporaryParameter,temporaryParameter,'+',1,)
                #save to stack
                generator.setStack(temporaryParameter,value.getValue())
                generator.newEnvironment(table.size)#new entorn
                generator.callFunction('consoleLogString')
                temporary=generator.addNewTemporary()
                generator.getStack(temporary,'P')
                #Return environment
                generator.returnEnvironment(table.size)
            elif value.getType()=="boolean":
                if isinstance(value.typeAssistant,List):
                    if value.labelTrue=='':
                        value.labelTrue=generator.addNewLabel()
                    if value.labelFalse=='':
                        value.labelFalse=generator.addNewLabel()
                temporaryLabel=generator.addNewLabel()
                generator.defineLabel(value.getLabelTrue())
                generator.consoleTrue()
                generator.addGotoLabel(temporaryLabel)
                generator.defineLabel(value.getLabelFalse())
                generator.consoleFalse()
                generator.defineLabel(temporaryLabel)
            
        generator.addConsoleLog('c',10)
