from Semantic.symbol_table import SymbolTable

class C3DGenerator:
    generator=None #var static
    def __init__(self):
        self.temporary_count=0#temporal count
        self.code=""#code
        self.temporaries=[]#temporals
        self.imports=[]
        self.start_imports=['fmt','math']
    ''' Structure '''
    #Get generator
    def getGenerator(self):
        if C3DGenerator.generator == None:
            C3DGenerator.generator = C3DGenerator
        return C3DGenerator.generator
    #clean
    def clear(self):
        self.temporary_count=0#temporal count
        self.code=""#code
        self.temporaries=[]#temporals
        self.imports=[]
        self.start_imports=['fmt','math']
        C3DGenerator.generator=C3DGenerator()# Para crear instancias
    #add imports
    def setImport(self,librery):
        if librery in self.start_imports:
            self.start_imports.remove(librery)
        else:
            return
        code=f'import(\n\t"{librery}"\n)\n'#formato
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
            code+="float64;\n\n"#int or decimal
        code+="var P, H float64;\nvar stack[30000000] float64;\nvar heap[30000000] float64;"#size array 3000000, stack=pile of symbol_table
        return code
    #get code
    def getCode(self):#obtain code
        return f'{self.getHead()}\nfunc main(){{\n{self.code}\n}}'
    #add new comment
    def addNewComment(self,comment):#create new comment
        self.code+=f'/*{comment}/*\n'
    #add new line
    def addNewLine(self):#create new line
        self.code+='\n'
    def addNewTemporary(self):#create new temporary, tInteger
        temporary=f't{self.temporary_count}'
        self.temporary_count+=1
        self.temporaries.append(temporary)
        return temporary 
    ''' Getter & Setter stack'''
    def setStack(self, position,value):
        self.code+=f'stack[int{position}] = {value};\n'
    def getStack(self, temporary,position):
        self.code+=f'{temporary} = stack[int{position}];\n'
    ''' Gettet, Setter & next heap'''
    def setHeap(self, position,value):
        self.code+=f'heap[int{position}] = {value};\n'
    def getHeap(self, temporary,position):
        self.code+=f'{temporary} = heap[int{position}];\n'
    def nextHeap(self):
        self.code+=f'H = H + 1;\n '
    ''' Environment'''
    #New environment
    def newEnvironment(self,size):#size for environment, P=pointer position in memory
        self.code+=f'/* New Environment */\nP = P + {size};\n'
    #Return environment
    def returnEnvironment(self,size):#size for environment
        self.code+=f'P = P - {size};\n/* Return Environment */\n'
    ''' Assignament '''
    def addNewAssignament(self,temporary,left):
        self.code+=f'{temporary} = {left};\n'
    ''' Expressions '''
    def addNewExpression(self,temporary,left,operator,right):
        self.code+=f'{temporary} = {left} {operator} {right};\n'
    ''' Call function'''
    def callFunction(self,id):
        self.code+=f'{id}();\n'
    ''' Console log'''
    def addConsoleLog(self, type, value):#type !%d=integer, %f=float, %c=character & %s=string
        self.setImport('fmt')
        self.codeIn(f'fmt.Printf("%{type}", int({value}));\n')

# console.log(4+5*6);