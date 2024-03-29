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
        self.plusString=False
        self.contrastToString=False
        self.nativeToUpperCase=False
        self.nativeToLowerCase=False
        self.arrayIndexError=False
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
        self.plusString=False
        self.contrastToString=False
        self.nativeToUpperCase=False
        self.nativeToLowerCase=False
        self.arrayIndexError=False
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
    ''' Console log True & False '''
    def consoleTrue(self):
        self.setImport('fmt')#write true
        self.addSpaceIdent()
        self.addConsoleLog("c", 116)#t
        self.addSpaceIdent()
        self.addConsoleLog("c", 114)#r
        self.addSpaceIdent()
        self.addConsoleLog("c", 117)#u
        self.addSpaceIdent()
        self.addConsoleLog("c", 101)#e
    def consoleFalse(self):
        self.setImport('fmt')#write false
        self.addSpaceIdent()
        self.addConsoleLog("c", 102)#f
        self.addSpaceIdent()
        self.addConsoleLog("c", 97)#a
        self.addSpaceIdent()
        self.addConsoleLog("c", 108)#l
        self.addSpaceIdent()
        self.addConsoleLog("c", 115)#s
        self.addSpaceIdent()
        self.addConsoleLog("c", 101)#e
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
        self.whereAddCode('return;\n}\n')
        if not self.onNative:
            self.onFunction=False
        

    ''' Expressions '''
    def addNewExpression(self,temporary,left,operator,right):
        if(operator=='^'):
            self.whereAddCode(f'{temporary} = math.Pow({left},{right});\n')
        elif(operator=='%'):
            self.whereAddCode(f'{temporary} = math.Mod({left},{right});\n')
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
        if(type=='f'):
            self.whereAddCode(f'fmt.Printf("%{type}", {value});\n')
        else:
            self.whereAddCode(f'fmt.Printf("%{type}", int({value}));\n')
            
    ''' Natives '''
    #print string
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
    
    #join string, string+string
    def joinString(self):
        if self.plusString:
            return
        self.plusString = True
        self.onNative = True
        self.addStartFunction('joinString')#start the function to join
        labelReturn = self.addNewLabel()#Create labelReturn
        labelFirst = self.addNewLabel()#Create labelFirst,labelSecond,labelThird
        labelSecond = self.addNewLabel()
        labelThird = self.addNewLabel()
        temporaryFirst = self.addNewTemporary()#add temporaryFirst,Second,Third, Fouth and Five
        temporarySecond = self.addNewTemporary()
        temporaryThird = self.addNewTemporary()
        temporaryFourth = self.addNewTemporary()
        temporaryFive = self.addNewTemporary()
        self.addNewExpression(temporaryFirst, 'H',"","")#add new expression, temporaryFirst=H
        self.addNewExpression(temporarySecond,'P','+','1')#temporarySecond=P+1
        self.getStack(temporaryFourth, temporarySecond)#temporaryFourth=stack[int(temporarySecond)]
        self.addNewExpression(temporaryThird, 'P', '+', '2')#temporaryThird=P+2
        self.defineLabel(labelFirst)#lFirst:
        self.addSpaceIdent()#espace
        self.getHeap(temporaryFive, temporaryFourth)#temporaryFive=heap[int(temporaryFourth)]
        self.addSpaceIdent()#espace
        self.addNewIf(temporaryFive, '-1','==', labelSecond)#if temporary ==-1 goto{labelSecond},  -1=end
        self.addSpaceIdent()#espace
        self.setHeap('H', temporaryFive)#heap[int(H)]=temporaryFive
        self.addSpaceIdent()#espace
        self.addNewExpression('H', 'H','+','1')#add one H, H=H+1
        self.addSpaceIdent()#espace
        self.addNewExpression(temporaryFourth,temporaryFourth, '+','1')#tFourth=tFourth+1, add 1
        self.addSpaceIdent()#espace
        self.addGotoLabel(labelFirst)#goto{labelFirst}
        self.defineLabel(labelSecond)#lSecond:
        self.addSpaceIdent()#espace
        self.getStack(temporaryFourth,temporaryThird)#tFourth=stack[int(tThird)]
        self.defineLabel(labelThird)#lThird:
        self.addSpaceIdent()#espace
        self.getHeap(temporaryFive, temporaryFourth)#tFive=heap[int(tFourth)]
        self.addSpaceIdent()#espace
        self.addNewIf(temporaryFive, '-1','==', labelReturn)#if tFive==-1, goto{labelReturn}, -1=end
        self.addSpaceIdent()#espace
        self.setHeap('H', temporaryFive)#heap[int(H)]=tFive
        self.addSpaceIdent()#espace
        self.addNewExpression('H','H','+','1')#add 1 to H, H=H+1
        self.addSpaceIdent()#espace
        self.addNewExpression(temporaryFourth,temporaryFourth,'+','1')#tFourth=tFourth+1, add +1
        self.addSpaceIdent()#espace
        self.addGotoLabel(labelThird)#goto{labelThird}
        self.defineLabel(labelReturn)#lReturn:
        self.addSpaceIdent()#espace
        self.setHeap('H', '-1')#heap[int(H)]=-1, end
        self.addSpaceIdent()#espace
        self.addNewExpression('H', 'H','+','1')#add 1 in H, H=H+1
        self.addSpaceIdent()#espace
        self.setStack('P', temporaryFirst)#set stack, stack[int(P)]=tFirst
        self.addEndFunction()#end function
        self.onNative = False#Reset onNative

    #compareString
    def contrastString(self):
        if self.contrastToString:
            return
        #add code on native not in main
        self.contrastToString = True
        self.onNative = True
        # Start function
        self.addStartFunction("contrastString")
        #Goto to move at label
        returnLabel=self.addNewLabel()
        temporaryStack = self.addNewTemporary()#temporary=P+1
        self.addNewExpression(temporaryStack, 'P', '+', '1')
        temporaryCallStack = self.addNewTemporary()#temporaryCallStack
        self.getStack(temporaryCallStack, temporaryStack)#temporaryCallStack= stack[int(temporary)]
        self.addNewExpression(temporaryStack,temporaryStack, '+','1')#temporary=temporary+1
        temporaryCallStack2 = self.addNewTemporary()#temporaryCallStack2 
        self.getStack(temporaryCallStack2, temporaryStack)#temporaryCallStack2= stack[int(temporary)]
        #create first,second and third label
        firstLabel = self.addNewLabel()
        secondLabel = self.addNewLabel()
        thirdLabel = self.addNewLabel()
        self.defineLabel(firstLabel)#define first label
        #temporarycall heap
        temporaryCallHeap = self.addNewTemporary()
        self.addSpaceIdent()
        self.getHeap(temporaryCallHeap,temporaryCallStack)#temporaryCallHeap=heap[temporaryCallStack]
        #temporaryCallHeap2
        temporaryCallHeap2 = self.addNewTemporary()
        self.addSpaceIdent()
        self.getHeap(temporaryCallHeap2,temporaryCallStack2)#temporaryCallHeap2=heap[temporaryCallStack2]

        self.addSpaceIdent()
        self.addNewIf(temporaryCallHeap,temporaryCallHeap2,'!=', thirdLabel)#if temporaryCallHeap != temporaryCallHeap2, goto third label
        self.addSpaceIdent()
        self.addNewIf(temporaryCallHeap,'-1', '==', secondLabel)#if temporaryCallHeap == -1, second label

        self.addSpaceIdent()
        self.addNewExpression(temporaryCallStack, temporaryCallStack, '+','1')#callstack+1
        self.addSpaceIdent()
        self.addNewExpression(temporaryCallStack2, temporaryCallStack2,'+','1')#callstack2+1
        self.addSpaceIdent()
        self.addGotoLabel(firstLabel)#goto first label

        self.defineLabel(secondLabel)#define second label
        self.addSpaceIdent()
        #set stack stack[int(P)]=1
        self.setStack('P', '1')
        self.addSpaceIdent()
        self.addGotoLabel(returnLabel)#goto return label
        self.defineLabel(thirdLabel)#define third label
        self.addSpaceIdent()
        #set stack stack[int(P)]=0
        self.setStack('P', '0')
        self.defineLabel(returnLabel)#goto return label
        self.addEndFunction()
        self.onNative = False
    #native upperCase
    def upperCase(self):
        if self.nativeToUpperCase:
            return
        self.nativeToUpperCase = True
        self.onNative = True 
        self.addStartFunction('toUpperCase')#Start with the function
        #Add new temporaries
        temporary = self.addNewTemporary()
        temporarySecond = self.addNewTemporary()
        temporaryThird = self.addNewTemporary()
        #Add labels
        label = self.addNewLabel()
        labelSecond = self.addNewLabel()
        labelThird = self.addNewLabel()
        #Create new assignament
        self.addNewAssignament(temporary, 'H')
        self.addNewExpression(temporarySecond, 'P','+', '1')#add the expression tSecond=P+1
        self.getStack(temporarySecond, temporarySecond)#temporary=stack[int(temporary)]
        self.defineLabel(label)#L:
        self.getHeap(temporaryThird, temporarySecond)#tThird=heap[int(tSecond)]
        #Compare to, only letters minus are in 97 and 122 ascii others no matter
        self.addNewIf(temporaryThird, '-1', '==', labelThird)#tThird==-1 lThird
        self.addNewIf(temporaryThird, '97', '<', labelSecond)#tThird<91 lSecond
        self.addNewIf(temporaryThird, '122', '>', labelSecond)#tThird>122 lSecond
        self.addNewExpression(temporaryThird, temporaryThird, '-', '32')#data minus 32 for change lower at upper
        self.defineLabel(labelSecond)#define labelSecond
        self.setHeap('H', temporaryThird)#set heap to temporaryThird
        self.nextHeap()#next
        self.addNewExpression(temporarySecond, temporarySecond, '+', '1')#tSecond=tSecond+1
        self.addGotoLabel(label)#Goto l
        self.defineLabel(labelThird)#lThird
        self.setHeap('H', '-1')#set heap to -1 (end)
        self.nextHeap()#next heap
        self.setStack('P', temporary)#set the stack with temporary
        self.addEndFunction()
        self.onNative = False
    #Native lowerCase
    def lowerCase(self):
        if self.nativeToLowerCase:
            return
        self.nativeToLowerCase = True
        self.onNative = True 
        self.addStartFunction('toLowerCase')#Start with the function
        #Add new temporaries
        temporary = self.addNewTemporary()
        temporarySecond = self.addNewTemporary()
        temporaryThird = self.addNewTemporary()
        #Add labels
        label = self.addNewLabel()
        labelSecond = self.addNewLabel()
        labelThird = self.addNewLabel()
        #Create new assignament
        self.addNewAssignament(temporary, 'H')
        self.addNewExpression(temporarySecond, 'P','+', '1')#add the expression tSecond=P+1
        self.getStack(temporarySecond, temporarySecond)#temporary=stack[int(temporary)]
        self.defineLabel(label)#L:
        self.getHeap(temporaryThird, temporarySecond)#tThird=heap[int(tSecond)]
        #Compare to, only letters minus are in 97 and 122 ascii others no matter
        self.addNewIf(temporaryThird, '-1', '==', labelThird)#tThird==-1 lThird
        self.addNewIf(temporaryThird, '65', '<', labelSecond)#tThird<65 lSecond
        self.addNewIf(temporaryThird, '90', '>', labelSecond)#tThird>90 lSecond
        self.addNewExpression(temporaryThird, temporaryThird, '+', '32')#data plus 32 for change upper at lower
        self.defineLabel(labelSecond)#define labelSecond
        self.setHeap('H', temporaryThird)#set heap to temporaryThird
        self.nextHeap()#next
        self.addNewExpression(temporarySecond, temporarySecond, '+', '1')#tSecond=tSecond+1
        self.addGotoLabel(label)#Goto l
        self.defineLabel(labelThird)#lThird
        self.setHeap('H', '-1')#set heap to -1 (end)
        self.nextHeap()#next heap
        self.setStack('P', temporary)#set the stack with temporary
        self.addEndFunction()
        self.onNative = False
    #typeOf
    #index error
    def indexError(self):
        if self.arrayIndexError:
            return
        self.arrayIndexError = True
        self.onNative = True
        self.addStartFunction('arrarIndexError')
        arrayError = "Index out range\n"
        for char in arrayError:#print array error
            self.addConsoleLog("c",ord(char))
        self.addEndFunction()
        self.addNewLine()
        self.onNative = False