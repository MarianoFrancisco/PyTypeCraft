from ..Semantic.symbol_table import SymbolTable

class C3DGenerator:
    generator=None #var static
    def __init__(self):
        # Count
        self.temporaryCount=0#temporal count
        self.labelCount=0
        # Code
        self.code=""#code
        self.temporaries=[]#temporals
        self.imports=[]
        #natives
        self.consoleLogString=False#Only in string, array or char
        # Verify if we're on function or native
        self.functions=''
        self.natives=''
        self.onFunction=False
        self.onNative=False 
        self.startImports=['fmt','math']
    ''' Structure '''
    #Get generator
    def getGenerator(self):
        if C3DGenerator.generator == None:
            C3DGenerator.generator = C3DGenerator()
        return C3DGenerator.generator
    #clean
    def clear(self):
        # Count
        self.temporaryCount=0#temporal count
        self.labelCount=0
        #code
        self.code=""
        self.temporaries=[]#temporals
        self.imports=[]
        #natives
        self.consoleLogString=False
        # Verify if we're on function or native
        self.functions=''
        self.natives=''
        self.onFunction=False
        self.onNative=False 
        self.startImports=['fmt','math']
        C3DGenerator.generator=C3DGenerator()# Para crear instancias
    #add imports
    def setImport(self,librery):
        if librery in self.startImports:
            self.startImports.remove(librery)
        else:
            return
        code=f'import(\n\t"{librery}"\n);\n'#formato
        self.imports.append(code)
    #get header
    def getHead(self):
        len_imports=len(self.imports)
        len_temporaries=len(self.temporaries)
        code='/*START CODE: MARIANO & MANUEL*/\npackage main;\n\n'
        if (len_imports>0):
            for temporary in self.imports:
                code +=temporary
        if (len_temporaries>0):#add var temporary
            code+='var '
            for temporary in self.temporaries:
                code+=temporary+','
            code=code[:-1]
            code+=" float64;\n\n"#int or decimal
        code+="var P, H float64;\nvar stack[30000000] float64;\nvar heap[30000000] float64;\n"#size array 3000000, stack=pile of symbol_table
        return code
    #get code
    def getCode(self):#obtain code
        return f'{self.getHead()}{self.natives}{self.functions}\nfunc main(){{\n{self.code}\n}}'
    #Add code in native or normal function
    def whereAddCode(self,code,ident='\t'):
        if self.onNative:
            if self.natives == '':
                self.natives = self.natives + '/* Start Natives */\n'
            self.natives=self.natives+ident+code
        elif self.onFunction:
            if self.functions == '':
                self.functions = self.functions + '/* Start Functions */\n'
            self.functions=self.functions+ident+code  
        else:
            self.code=self.code+'\t'+code
    #add new comment
    def addNewComment(self,comment):#create new comment
        self.whereAddCode(f'/*{comment}*/\n')
    #add new line
    def addNewLine(self):#create new line
        self.whereAddCode('\n')
    def addNewTemporary(self):#create new temporary, tInteger
        temporary=f't{self.temporaryCount}'
        self.temporaryCount+=1
        self.temporaries.append(temporary)
        return temporary 
    ''' Getter & Setter stack'''
    def setStack(self, position,value):
        self.whereAddCode(f'stack[int({position})] = {value};\n')
    def getStack(self, temporary,position):
        self.whereAddCode(f'{temporary} = stack[int({position})];\n')
    ''' Gettet, Setter & next heap'''
    def setHeap(self, position,value):
        self.whereAddCode(f'heap[int({position})] = {value};\n')
    def getHeap(self, temporary,position):
        self.whereAddCode(f'{temporary} = heap[int({position})];\n')
    def nextHeap(self):
        self.whereAddCode(f'H = H + 1;\n')
    ''' Labels '''
    def addNewLabel(self):#To move into instructions
        label=f'L{self.labelCount}'
        self.labelCount+=1
        return label
    def defineLabel(self,label):#L1:L2
        self.whereAddCode(f'{label}:\n')
    # Space ident
    def addSpaceIdent(self):
        self.whereAddCode("")
    ''' Goto '''
    def addGotoLabel(self,label):
        self.whereAddCode(f'goto {label};\n')
    ''' Environment'''
    #New environment
    def newEnvironment(self,size):#size for environment, P=pointer position in memory
        self.whereAddCode(f'/* New Environment */\nP = P + {size};\n')
    #Return environment
    def returnEnvironment(self,size):#size for environment
        self.whereAddCode(f'P = P - {size};\n/* Return Environment */\n')
    ''' Assignament '''
    def addNewAssignament(self,temporary,left):
        self.whereAddCode(f'{temporary} = {left};\n')
    ''' Conditional IF '''
    def addNewIf(self, left, right, operator, label):
        self.whereAddCode(f'if {left} {operator} {right} {{goto {label};}}\n')
    ''' Functions'''
    def addStartFunction(self,id):
        if (not self.onNative):#If not native is a normal function
            self.onFunction=True
        self.whereAddCode(f'func {id}(){{\n','')
    def addEndFunction(self):
        if not self.onNative:
            self.onFunction=False
        self.whereAddCode('\n}\n')

    ''' Expressions '''
    def addNewExpression(self,temporary,left,operator,right):
        if(operator=='^'):
            self.whereAddCode(f'{temporary} = math.Pow({left},{right});\n')
        elif(operator=='==='):
            self.whereAddCode(f'{temporary} = {left} == {right};\n')
        elif(operator=='!=='):
            self.whereAddCode(f'{temporary} = {left} != {right};\n')
        else:
            self.whereAddCode(f'{temporary} = {left} {operator} {right};\n')
    ''' Call function '''
    def callFunction(self,id):
        self.whereAddCode(f'{id}();\n')
    ''' Console log '''
    def addConsoleLog(self, type, value):#type !%t=boolean, %f=float, %c=character & %s=string
        self.setImport('fmt')
        self.whereAddCode(f'fmt.Printf("%{type}", int({value}));\n')
    ''' Natives '''
    def consoleString(self):
        self.setImport('fmt')
        if(self.consoleLogString):#True only return
            return
        self.consoleLogString=True#Cambios su valor a True
        self.onNative=True
        #Add in the start
        self.addStartFunction('consoleLogString')
        #Goto to move at label
        returnLabel=self.addNewLabel()
        compareLabel=self.addNewLabel()
        temporaryStack=self.addNewTemporary()#Pointer stack
        temporaryHeap=self.addNewTemporary()#Pointer heap
        self.addNewExpression(temporaryStack,'P','+','1')
        self.getStack(temporaryHeap,temporaryStack)
        temporaryCompare=self.addNewTemporary()
        self.defineLabel(compareLabel)
        self.addSpaceIdent()#add ident
        self.getHeap(temporaryCompare,temporaryHeap)#Compare temporary with heap
        self.addSpaceIdent()
        self.addNewIf(temporaryCompare,'-1','==',returnLabel)#-1 is end
        self.addConsoleLog('c',temporaryCompare)
        self.addSpaceIdent()
        self.addNewExpression(temporaryHeap,temporaryHeap,'+','1')#Plus one to heap
        self.addGotoLabel(compareLabel)
        self.defineLabel(returnLabel)
        self.addEndFunction()
        self.onNative=False
