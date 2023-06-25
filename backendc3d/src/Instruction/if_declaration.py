from ..Semantic.c3d_generator import C3DGenerator
from ..Semantic.exception import CompilerException
from ..Semantic.symbol_table import SymbolTable
from ..Abstract.abstract import Abstract
from ..Instruction.reserved_return import ReservedReturn
from ..Instruction.reserved_continue import ReservedContinue
from ..Instruction.reserved_break import ReservedBreak

class IfSentence(Abstract):

    def __init__(self, condition, ifBlock, elseBlock, elseIfBlock, line, column):
        super().__init__(line, column)
        self.condition = condition
        self.ifBlock = ifBlock
        self.elseBlock = elseBlock
        self.elseIfBlock = elseIfBlock
    

    def execute(self, tree, table):
        callGenerator=C3DGenerator()
        generator=callGenerator.getGenerator()
        generator.addNewComment('Start conditional if')
        condition = self.condition.execute(tree, table) # True o False
        if isinstance(condition, CompilerException) : return condition

        if condition.getType() == 'boolean':
            generator.defineLabel(condition.getLabelTrue())
            entorn = SymbolTable(table)  #New entorn
            for instruction in self.ifBlock:
                entorn.labelBreak = table.labelBreak#exit of all if
                entorn.labelContinue = table.labelContinue#continue with the if
                entorn.labelReturn = table.labelReturn#return data
                valueInstruction = instruction.execute(tree, entorn)#execute de instruction
                if isinstance(valueInstruction, CompilerException):
                    tree.setExceptions(valueInstruction)
                if isinstance(valueInstruction, ReservedBreak):
                    if table.labelBreak != '':
                        generator.addGotoLabel(table.labelBreak)#goto{table.labelBreak}
                    else:
                        leave = generator.addNewLabel()#add new label (leave)
                        generator.addGotoLabel(leave)#goto{leave(the new label)}
                        generator.defineLabel(valueInstruction.getLabel())#L(valueInstruction.label):
                        generator.defineLabel(leave)#Lleave:
                        return CompilerException("Semantico", "Error: Break fuera de la instancia", self.line, self.column)
                if isinstance(valueInstruction, ReservedContinue):
                    if table.labelContinue != '':
                        generator.addGotoLabel(table.labelContinue)#goto{table.labelContinue}
                    else:
                        gotoContinue = generator.addNewLabel()#add new label (gotocontinue)
                        generator.addGotoLabel(gotoContinue)#goto{gotoContinue}
                        generator.defineLabel(condition.getLabelFalse())#label condition.labelFalse
                        generator.defineLabel(gotoContinue)#gotoContinue:
                        return CompilerException("Semantico", "Error: Continue fuera de la instancia", self.line, self.colum)
                if isinstance(valueInstruction, ReservedReturn):#if is instance ofreturn
                    if entorn.labelReturn != '':
                        generator.addNewComment('Return data for the function')
                        if valueInstruction.getLabelTrue() == '':#verify getLabel, if is '' set the stack with valueInstruction
                            generator.setStack('P', valueInstruction.getValue())
                            generator.addGotoLabel(entorn.labelReturn)#Add gotolabel return label
                        else:
                            generator.defineLabel(valueInstruction.getLabelTrue())#if exist, define my label true
                            generator.setStack('P', '1')#set the stack in the position 1
                            generator.addGotoLabel(entorn.labelReturn)#return label and define label to label false
                            generator.defineLabel(valueInstruction.getLabelFalse())
                            generator.setStack('P', '0')
                            generator.addGotoLabel(entorn.labelReturn)#set stack =0 and goto label to return label
                        generator.addNewComment('End return data for the function')
            #greate label to leave
            leave = generator.addNewLabel()
            generator.addGotoLabel(leave)
            generator.defineLabel(condition.getLabelFalse())
            if self.elseBlock != None:
                entorn = SymbolTable(table)  #New entorn
                for instruction in self.elseBlock:#instruction for block else
                    entorn.labelBreak = table.labelBreak#exit of all else
                    entorn.labelContinue = table.labelContinue#continue with the else
                    entorn.labelReturn = table.labelReturn#return data
                    valueInstruction = instruction.execute(tree, entorn)#execute de instruction
                    if isinstance(valueInstruction, CompilerException):
                        tree.setExceptions(valueInstruction)
                    if isinstance(valueInstruction, ReservedReturn):#if is instance of reserved return
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
            elif self.elseIfBlock != None:#obtain instruction for block else if
                resultElseIf = self.elseIfBlock.execute(tree,table)
                if isinstance(resultElseIf, CompilerException): return resultElseIf
            generator.defineLabel(leave)#define my lave for leave, L#:
        generator.addNewComment('End conditional if')

        # conditionEvaluated = self.condition.execute(tree, table)
        # if isinstance(conditionEvaluated, CompilerException): return conditionEvaluated
        # # Validar que el tipo sea booleano
        # if bool(conditionEvaluated) == True:
        #     scope = SymbolTable(table)  #NUEVO ENTORNO - HIJO - Vacio
        #     for instruccion in self.ifBlock:
        #         result = instruccion.execute(tree, scope) 
        #         if isinstance(result, CompilerException) :
        #             tree.setExceptions(result)
        #         if isinstance(result, ReservedReturn): return result
        # elif self.elseBlock != None:
        #     scope = SymbolTable(table)
        #     for instruccion in self.elseBlock:
        #         result = instruccion.execute(tree, scope) 
        #         if isinstance(result, CompilerException) :
        #             tree.setExceptions(result)
        #         if isinstance(result, ReservedReturn): return result
        # elif self.elseIfBlock != None:
        #     result = self.elseIfBlock.execute(tree, table)
        #     if isinstance(result, ReservedReturn): return result
