from ..Semantic.symbol import Symbol
from ..Semantic.exception import CompilerException
from ..Abstract.abstract import Abstract
from ..Semantic.symbol_table import SymbolTable
from ..Semantic.c3d_generator import C3DGenerator
from ..Instruction.reserved_return import ReservedReturn
from ..Instruction.reserved_break import ReservedBreak
from ..Instruction.reserved_continue import ReservedContinue
from ..Expression.binary_operation import ArithmeticOperation,RelationalOperation,LogicOperation

class For(Abstract):

    def __init__(self, requirement, restriction, variation, instructions, line,column):
        self.requirement = requirement
        self.restriction = restriction
        self.variation = variation
        self.instructions = instructions
        super().__init__(line,column)
    
    def execute(self, tree, table):
        callGenerator=C3DGenerator()
        generator=callGenerator.getGenerator()
        generator.addNewComment('Start loop for')
        entorn = SymbolTable(table)#New entorn
        requirement=self.requirement.execute(tree,table)#execute declaration
        if isinstance(requirement, CompilerException): return requirement
        if isinstance(self.restriction,RelationalOperation):
            operator = self.restriction.operator
        else:
            generator.addNewComment('Error: No hay operacion relacional en el for')
            return self.restriction
        while True:
            #Verify if is operator correct
            if (operator=='>' or operator=='<' or operator=='<=' or operator=='>=' or operator=='===' or operator=='!==' or operator=='&&' or operator=='||'):
                entorn2 = SymbolTable(table)#New entorn
                labelFirst = generator.addNewLabel()
                generator.defineLabel(labelFirst)#define label create before
                restriction = self.restriction.execute(tree, table)#execute the restriction
                if isinstance(restriction, CompilerException): #add exception if is instance of compiler exception
                    tree.setExceptions(restriction)
                generator.defineLabel(restriction.getLabelTrue())#define the label trues
                #End label false, continue label first
                table.labelBreak = restriction.getLabelFalse()
                table.labelContinue = labelFirst
                for instruction in self.instructions:
                    entorn.labelBreak = table.labelBreak#exit of all else
                    entorn.labelContinue = table.labelContinue#continue with the else
                    entorn.labelReturn = table.labelReturn#return data
                    valueInstruction = instruction.execute(tree, entorn2)#execute de instruction
                    if isinstance(valueInstruction, CompilerException):
                        tree.setExceptions(valueInstruction)
                    if isinstance(valueInstruction, ReservedBreak):#Break to end the function
                        generator.addGotoLabel(table.labelBreak)#Redirect to end
                    if isinstance(valueInstruction, ReservedContinue):#Continue return to the first label
                        generator.addGotoLabel(table.labelContinue)
                    if isinstance(valueInstruction, ReservedReturn):#if is instance of reserved return
                        if entorn.labelReturn != '':
                            generator.addNewComment('Return data for the function')
                            if valueInstruction.getLabelTrue() == '':#if labeltrue ='' set the stack with instruction value
                                generator.setStack('P', valueInstruction.getValue())
                                generator.addGotoLabel(entorn.labelReturn)#add goto label to return label
                            else:
                                generator.defineLabel(valueInstruction.getLabelTrue())#define label with instruction for label true
                                generator.setStack('P', '1')#set the stack with 1
                                generator.addGotoLabel(entorn.labelReturn)#add goto label to return label
                                generator.defineLabel(valueInstruction.getLabelFalse())#define
                                generator.setStack('P', '0')#set the stack to 0 and goto label to return label
                                generator.addGotoLabel(entorn.labelReturn)
                        generator.addNewComment('End return data for the function')
                variation = self.variation.execute(tree, entorn)
                if isinstance(variation, CompilerException): return variation
                #Reset labels on table
                table.labelBreak = ''
                table.labelContinue= ''
                #Redirect
                generator.addGotoLabel(labelFirst)#Goto to first label
                generator.defineLabel(restriction.getLabelFalse())#define end
                generator.addNewComment("End loop for")
            break
        
class ForOf(Abstract):

    def __init__(self, declaration, array, instructions, line,column):
        self.declaration = declaration
        self.array = array
        self.instructions = instructions
        super().__init__(line,column)
    
    def execute(self, tree, table):
        return None


