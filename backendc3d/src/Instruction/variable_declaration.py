from ..Expression.array import Array
from ..Expression.primitive import Primitive
from ..Semantic.exception import CompilerException
from ..Abstract.abstract import Abstract
from ..Semantic.c3d_generator import C3DGenerator
from ..Expression.identifier import Identifier
from ..Semantic.symbol import Symbol

class VariableDeclaration(Abstract):

    def __init__(self, id, type, value, line, column):
        self.id = id
        self.type = type
        self.value = value
        super().__init__(line, column)
        self.search=True
        self.hide=-1
        # ASIGNANDO VALORES POR DEFECTO
        if value == None:
            if type == 'number':
                self.value = Primitive(0, 'number', self.line, self.column)
            elif type == 'boolean':
                self.value = Primitive(False, 'boolean', self.line, self.column)
            elif type == 'string':
                self.value = Primitive('', 'string', self.line, self.column)
            else:
                self.value = None
    
    def execute(self, tree, table):
        callGenerator=C3DGenerator()
        generator=callGenerator.getGenerator()
        generator.addNewComment('Variable declaration')
        
        # Verificacion de types
        if hasattr(self.value, 'id') and isinstance(self.value, Identifier):
            value = table.getSymbolById(self.value.id)
            dataType=value.type
        else:
            value = self.value.execute(tree, table)
            dataType=self.value.type
        if isinstance(value, CompilerException): return value 
        if 'Array' in self.type and not isinstance(self.value, Array):
            return CompilerException("Semantico", f"La expresion {value} no puede asignarse a '{self.id}', ya que no es un arreglo", self.line, self.column)
        if self.type != 'any' and not ('Array' in self.type) and isinstance(self.value, Array):
            return CompilerException("Semantico", f"La variable '{self.id}' no se le puede asignar un arreglo", self.line, self.column)
        if 'any' in str(self.type) or str(dataType) in str(self.type):
            inHeap=value.getType()=='string' or value.getType()=='interface'
            symbol = table.setTable(self.id,value.type,inHeap,self.search)
        else:
            generator.addNewComment('Error: Tipo de dato es diferente al declarado')
            result = CompilerException("Semantico", "Tipo de dato es diferente al declarado", self.line, self.column)
            return result
        temporaryPosition=symbol.position
        if not symbol.isGlobal:
            temporaryPosition=generator.addNewTemporary()
            generator.addNewExpression(temporaryPosition, 'P', '+', symbol.position)
        if value.getType() == 'boolean':
            temporaryLabel = generator.addNewLabel()
            
            generator.defineLabel(value.labelTrue)
            generator.setStack(temporaryPosition, "1")
            
            generator.addGotoLabel(temporaryLabel)

            generator.defineLabel(value.labelFalse)
            generator.setStack(temporaryPosition, "0")

            generator.defineLabel(temporaryLabel)
        else:
            if isinstance(value, Symbol):
                temporary=generator.addNewTemporary()#create new temporary
                generator.getStack(temporary,value.position)
                generator.setStack(symbol.position,temporary)
            else:
                generator.setStack(temporaryPosition,value.getValue())
        generator.addNewComment('End variable declaration')
        
    