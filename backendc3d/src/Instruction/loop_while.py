from ..Semantic.c3d_generator import C3DGenerator
from ..Semantic.symbol_table import SymbolTable
from ..Semantic.exception import CompilerException
from ..Abstract.abstract import Abstract
from ..Instruction.reserved_return import ReservedReturn
from ..Instruction.reserved_break import ReservedBreak
from ..Instruction.reserved_continue import ReservedContinue

class While(Abstract):

    def __init__(self, condition, instructions, line, column):
        self.condition = condition
        self.instructions = instructions
        super().__init__(line, column)

    def execute(self, tree, table):
        # call the generator
        callGenerator=C3DGenerator()
        generator=callGenerator.getGenerator()
        generator.addNewComment("Start loop while")
        operator = self.condition.operator
        while True:
            #Verify if is operator correct
            if (operator=='>' or operator=='<' or operator=='<=' or operator=='>=' or operator=='===' or operator=='!==' or operator=='&&' or operator=='||'):
                labelFirst = generator.addNewLabel()
                generator.defineLabel(labelFirst)#define label create before
                condition = self.condition.execute(tree, table)#execute the condition
                if isinstance(condition, CompilerException): #add exception if is instance of compiler exception
                    tree.setExceptions(condition)
                generator.defineLabel(condition.getLabelTrue())#define the label trues
                #End label false, continue label first
                table.labelBreak = condition.getLabelFalse()
                table.labelContinue = labelFirst
                for instruction in self.instructions:
                    entorn = SymbolTable(table)  #New entorn
                    entorn.labelBreak = table.labelBreak#exit of all else
                    entorn.labelContinue = table.labelContinue#continue with the else
                    entorn.labelReturn = table.labelReturn#return data
                    valueInstruction = instruction.execute(tree, entorn)#execute de instruction
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
                #Reset labels on table
                table.labelBreak = ''
                table.labelContinue= ''
                #Redirect
                generator.addGotoLabel(labelFirst)#Goto to first label
                generator.defineLabel(condition.getLabelFalse())#define end
                generator.addNewComment("End loop while")
            break