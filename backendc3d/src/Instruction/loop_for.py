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
        """ entorn = SymbolTable(table)
        localVariable = self.declaration.execute(tree, entorn)
        if isinstance(localVariable, CompilerException): return localVariable

        arr = self.array.execute(tree, entorn)
        if isinstance(arr, CompilerException): return arr

        if not isinstance(arr, str) and not isinstance(arr, list):
            return CompilerException("Semantico", f"El valor no es un iterable", self.line, self.column)
        
        for i in range(len(arr)):
            primitive = Primitive(arr[i], self.array.type, self.array.line, self.array.column)
            result = VariableAssignation(self.declaration.id, primitive, primitive.line, primitive.column).execute(tree, entorn)
            if isinstance(result, CompilerException): return result
            for instruction in self.instructions:
                resultInstruction = instruction.execute(tree, entorn)
                if isinstance(resultInstruction, CompilerException):
                    tree.setExceptions(result)
                    return resultInstruction
                if isinstance(resultInstruction, ReservedReturn): return resultInstruction
                if isinstance(resultInstruction, ReservedBreak): return None
                if isinstance(resultInstruction, ReservedContinue): break """
        return None
        """ flag = True
        entorn = table
        if table.searchSymbolById(self.requirement.id):#search for the first declaration
            flag = False#search if exist id

         """
        # nuevaTabla = TablaSimbolos(tabla)  # NUEVO ENTORNO

        # inicio = self.inicio.interpretar(arbol, nuevaTabla)
        # if isinstance(inicio, Excepcion): return inicio

        # condicion = self.condicion.interpretar(arbol, nuevaTabla)
        # if isinstance(condicion, Excepcion): return condicion
        # # Validar que el tipo sea booleano
        # if self.condicion.tipo != 'boolean':
        #     return Excepcion("Semantico", "Tipo de dato no booleano en FOR.", self.fila, self.columna)
        # # Recorriendo las instrucciones
        # while condicion:
        #     for instruccion in self.bloqueFor:
        #         result = instruccion.interpretar(arbol, nuevaTabla)
        #         if isinstance(result, Excepcion):
        #             arbol.excepciones.append(result)
            
        #     nuevo_valor = self.aumento.interpretar(arbol, nuevaTabla)
        #     if isinstance(nuevo_valor, Excepcion): return nuevo_valor
            
        #     simbolo = Simbolo(self.inicio.ide, self.inicio.tipo, nuevo_valor, self.fila, self.columna)

        #     # Actualizando el valor de la variable en la tabla de simbolos
        #     valor = nuevaTabla.updateTabla(simbolo)

        #     if isinstance(valor, Excepcion): return valor

        #     condicion = self.condicion.interpretar(arbol, nuevaTabla)
        #     if isinstance(condicion, Excepcion): return condicion
        #     if self.condicion.tipo != 'boolean':
        #         return Excepcion("Semantico", "Tipo de dato no booleano en FOR.", self.fila, self.columna)
        # return None
        # entorn = SymbolTable(table)
        # requirement = self.requirement.execute(tree, entorn)
        # if isinstance(requirement, CompilerException): return requirement

        # restriction = self.restriction.execute(tree, entorn)
        # if isinstance(restriction, CompilerException): return restriction
        # # Validar que el tipo sea booleano
        # if self.restriction.type != 'boolean':
        #     return CompilerException("Semantico", "Tipo de dato no booleano en FOR.", self.line, self.column)
        # # Recorriendo las instrucciones
        # while restriction:
        #     for instruction in self.instruction:
        #         result = instruction.execute(tree, entorn)
        #         if isinstance(result, CompilerException):
        #             tree.exceptions.append(result)
        #     variation = self.variation.execute(tree, entorn)
        #     if isinstance(variation, CompilerException): return variation
        #     symbol = Symbol(self.requirement.id, self.requirement.type, variation, self.line, self.column)
        #     # Actualizando el valor de la variable en la tabla de simbolos
        #     value = entorn.updateSymbol(symbol)

        #     if isinstance(value, CompilerException): return value

        #     restriction = self.restriction.execute(tree, entorn)
        #     if isinstance(restriction, CompilerException): return restriction
        #     if self.restriction.type != 'boolean':
        #         return CompilerException("Semantico", "Tipo de dato no booleano en FOR.", self.line, self.column)
        # return None
            


