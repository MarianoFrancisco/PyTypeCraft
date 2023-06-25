from ..Semantic.c3d_generator import C3DGenerator
from ..Abstract.abstract import Abstract
from ..Semantic.exception import CompilerException
from ..Abstract.return_data import ReturnData
from ..Instruction.reserved_return import ReservedReturn
#from ..Semantic.symbol import Symbol
#from ..Semantic.symbol_table import SymbolTable

class CallFunction(Abstract):

    def __init__(self, name,parameters,line,column):
        self.name = name
        self.parameters = parameters
        self.labelTrue=''
        self.labelFalse=''
        super().__init__(line,column)
    
    def execute(self, tree,table):
        callGenerator=C3DGenerator()
        generator=callGenerator.getGenerator()
        function = tree.getFunction(self.name)#call the function
        if function != None:
            generator.addNewComment(f'Call function {self.name}')
            parametersValue = []#all value parameter
            temporaries = []#my temporaries
            size = table.size#size of the environment
            for parameter in self.parameters:
                if isinstance(parameter,CallFunction):
                    self.saveTemporaries(generator, table, temporaries)#call save my temporaries
                    valueParemeter = parameter.execute(tree, table)#obtain value parameter
                    if isinstance(valueParemeter, CompilerException): return valueParemeter
                    parametersValue.append(valueParemeter)#add value parameter
                    self.getTemporaries(generator, table, temporaries)#get my temporaries
                else:
                    value = parameter.execute(tree, table)#execute
                    if isinstance(value, CompilerException):#if is exception only return
                        return value
                    parametersValue.append(value)#add value
                    temporaries.append(value.getValue())#add temporaries
            temporary = generator.addNewTemporary()
            generator.addNewExpression(temporary,'P', '+',size+1)
            count = 0
            if len(function.getParameters()) == len(parametersValue):#compair the parameter call with the function
                for parameter in parametersValue:
                    if function.parameters[count]['type'] == parameter.getType():#view the type of call and the function
                        count += 1
                        generator.setStack(temporary,parameter.getValue())
                        if count != len(parametersValue):#End when count = size parametersValue, else temporary=temporary+1
                            generator.addNewExpression(temporary,temporary,'+',1)
                    else:
                        generator.addNewComment(f'Error: End call function {self.name}')
                        return CompilerException("Semantico", f"Tipos distintos a los solicitados en los parametros {self.name}", self.line, self.column)

            generator.newEnvironment(size)
            #self.getFunction(function,generator) #Call function native
            self.getFunction(generator) #Call function native
            generator.callFunction(function.name)
            generator.getStack(temporary,'P')#obtain stack
            generator.returnEnvironment(size)#return the environment
            generator.addNewComment(f'End call function {self.name}')
            generator.addNewLine()

            if function.getType() != 'boolean':#distinct of the boolean
                return ReturnData(temporary, function.getType(), True)
            else:
                generator.addNewComment('Recover boolean')
                #verify to create or not
                if self.labelTrue == '':
                    self.labelTrue = generator.addNewLabel()
                if self.labelFalse == '':
                    self.labelFalse = generator.addNewLabel()
                #add new if to boolean
                generator.addNewIf(temporary,1,'==',self.labelTrue)
                generator.addGotoLabel(self.labelFalse)
                #Reserver return have the label true & false
                returnData = ReservedReturn(temporary, function.getType(), True)
                returnData.labelTrue = self.labelTrue
                returnData.labelFalse = self.labelFalse
                generator.addNewComment('End recover boolean')
                return returnData
        else:
            return CompilerException("Semantico", "No se encontro la funcion: " + str(self.name), str(self.line), str(self.column))
        
    def saveTemporaries(self, generator, table, temporaryParameter):
        generator.addNewComment('Start save temporaries')
        newTemporary = generator.addNewTemporary()#create new temporary
        for temporary in temporaryParameter:#
            generator.addNewExpression(newTemporary, 'P', '+', table.size)
            generator.setStack(newTemporary, temporary)#Save in new temporary my data
            table.size += 1#add 1
        generator.addNewComment('End save temporaries')
    
    def getTemporaries(self, generator, table, temporaryParameter):
        generator.addNewComment('Get save temporaries')
        newTemporary = generator.addNewTemporary()#create new temporary
        for temporary in temporaryParameter:#
            table.size -= 1#minus 1
            generator.addNewExpression(newTemporary, 'P', '+', table.size)
            generator.getStack(temporary,newTemporary)#Get the data
        generator.addNewComment('End get temporaries')

    # def getFunction(self,function,generator):
    #     if self.name == 'toUpperCase':
    #         generator.upperCase()
    #         function.setType('string')
    #     elif self.name == 'toLowerCase':
    #         generator.lowerCase()
    #         function.setType('string')
    #     return
    def getFunction(self,generator):
        if self.name == 'toUpperCase':
            generator.upperCase()
        elif self.name == 'toLowerCase':
            generator.lowerCase()
        return
        # function = tree.getFunction(self.name)
        # if function == None:
        #     return CompilerException("Semantico", "No se encontro la funcion: " + str(self.name), str(self.line), str(self.column))
        # entorn = SymbolTable(tree.getGlobalScope())
        # if len(self.parameters) == len(function.parameters):
        #     count = 0
        #     for expression in self.parameters:
                
        #         result_expression = expression.execute(tree, table)
                
        #         if isinstance(result_expression, CompilerException): return result_expression
                
        #         if function.parameters[count]['type'] == expression.type:
        #             symbol = Symbol(str(function.parameters[count]['id']), expression.type, result_expression, self.line, self.column)
        #             result = entorn.setTableFunction(symbol)
        #             if isinstance(result, CompilerException): return result
        #         elif function.parameters[count]['type']=='any':
        #             symbol = Symbol(str(function.parameters[count]['id']), expression.type, result_expression, self.line, self.column)
        #             result = entorn.setTableFunction(symbol)
        #             if isinstance(result, CompilerException): return result
        #         elif function.parameters[count]["type"]=="NoType":
        #             symbol = Symbol(str(function.parameters[count]['id']), expression.type, result_expression, self.line, self.column)
        #             result = entorn.setTableFunction(symbol)
        #             if isinstance(result, CompilerException): return result
        #         else:
        #             if(self.name=="toLowerCase"):
        #                 return CompilerException("Semantico", "La funcion nativa toLowerCase unicamente acepta string como parametro", str(-1), str(-1))
        #             elif(self.name=="length"):
        #                 return CompilerException("Semantico", "La funcion nativa length unicamente acepta string o array como parametro", str(-1), str(-1))
        #             elif(self.name=="toExponential"):
        #                 return CompilerException("Semantico", "La funcion nativa toExponential unicamente acepta string como parametros", str(-1), str(-1))
        #             elif(self.name=="toUpperCase"):
        #                 return CompilerException("Semantico", "La funcion nativa toUpperCase unicamente acepta string como parametro", str(-1), str(-1))
        #             elif(self.name=="toFixed"):
        #                 return CompilerException("Semantico", "La funcion nativa toFixed unicamente acepta number como parametros", str(-1), str(-1))
        #             elif(self.name=="split"):
        #                 return CompilerException("Semantico", "La funcion nativa split unicamente acepta string como parametros", str(-1), str(-1))
        #             else:
        #                 return CompilerException("Semantico", "Tipo de dato diferente en Parametros en la funcion "+self.name, str(self.line), str(self.column))
        #         count += 1
        
        # value = function.execute(tree, entorn) # me puede retornar un valor
        # if isinstance(value, CompilerException): return value
        # self.type = function.type
        # return value
