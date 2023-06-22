from ..Instruction.reserved_return import ReservedReturn
from typing import List
from ..Abstract.abstract import Abstract
from ..Semantic.exception import CompilerException
from ..Semantic.symbol_table import SymbolTable
from ..Semantic.c3d_generator import C3DGenerator

class Function(Abstract):

    def __init__(self, name, parameters, instructions, line,column):
        self.name = name
        self.parameters = parameters
        self.instructions = instructions
        self.type = 'number'
        self.retainTemporary=True#To go at other environment
        super().__init__(line,column)
    

    def execute(self, tree,table):
        function = tree.setFunctions(self.name, self)#set te function to verify
        if function == 'error':
            error = CompilerException("Semantico", f"Error: La funcion {self.name} ya existe", self.line, self.column)
            return error
        # call the generator
        callGenerator=C3DGenerator()
        generator=callGenerator.getGenerator()
        generator.addNewComment(f'Start function {self.name}')
        #create a entorn
        entorn = SymbolTable(table)
        #We need the first label to return
        labelReturn = generator.addNewLabel()
        entorn.labelReturn = labelReturn
        entorn.size = 1 #reset to one for the first space memory is 0
        if self.parameters != None:
            for parameter in self.parameters:
                if parameter['type'] == 'struct':#space for struct
                    symbol = entorn.setTable(parameter['id'], parameter['type'], True)
                elif not isinstance(parameter['type'], List):#for list of parameters
                    symbol = entorn.setTable(parameter['id'], parameter['type'], (parameter['type'] == 'string' or parameter['type'] == 'array' or parameter['type'] == 'struct'))
                else:
                    symbol = entorn.setTable(parameter['id'], parameter['type'][0], True)
                    symbol.setTypeAssistant(parameter['type'][1])
                    if parameter['type'][0] == 'struct':
                        struct = tree.getStruct(parameter['type'][1])
                        symbol.setParameters(struct.getParameters())
        generator.addStartFunction(self.name)
        for instruction in self.instructions:
            valueInstruction= instruction.execute(tree, entorn)#view instructions
            if isinstance(valueInstruction, CompilerException):
                tree.setExcepctions(valueInstruction)
            if isinstance(valueInstruction, ReservedReturn):
                generator.addNewComment('Start data into function')
                if valueInstruction.getLabelTrue() == '':
                    generator.setStack('P',valueInstruction.value)
                    generator.addGotoLabel(entorn.labelReturn)
                else:
                    generator.defineLabel(valueInstruction.getLabelTrue())
                    generator.setStack('P', '1')
                    generator.addGotoLabel(entorn.labelReturn)
                    generator.defineLabel(valueInstruction.getLabelFalse())
                    generator.setStack('P', '0')
                    generator.addGotoLabel(entorn.labelReturn)
                generator.addNewComment('End of data into function')
        generator.addGotoLabel(labelReturn)
        generator.defineLabel(labelReturn)
        generator.addNewComment(f'End function {self.name}')
        generator.addEndFunction()
        generator.addNewLine()
        return
    '''Getters'''
    def getParameters(self):
        return self.parameters

    def getType(self):
        return self.type