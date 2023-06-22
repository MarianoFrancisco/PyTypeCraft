from ..Expression.array import Array
from ..Expression.primitive import Primitive
from ..Semantic.exception import CompilerException
from ..Abstract.abstract import Abstract
from ..Semantic.c3d_generator import C3DGenerator

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
        value = self.value.execute(tree, table)
        if isinstance(value, CompilerException): return value 
        # Verificacion de types
        if 'Array' in self.type and not isinstance(self.value, Array):
            return CompilerException("Semantico", f"La expresion {value} no puede asignarse a '{self.id}', ya que no es un arreglo", self.line, self.column)
        if self.type != 'any' and not ('Array' in self.type) and isinstance(self.value, Array):
            return CompilerException("Semantico", f"La variable '{self.id}' no se le puede asignar un arreglo", self.line, self.column)
        if 'any' in str(self.type) or str(self.value.type) in str(self.type):
            inHeap=value.getType()=='string' or value.getType()=='interface'
            symbol = table.setTable(self.id,value.type,inHeap,self.search)
        else:
            generator.addNewComment('Error: Tipo de dato es diferente al declarado')
            result = CompilerException("Semantico", "Tipo de dato es diferente al declarado", self.line, self.column)
            return result
        temporaryPosition=symbol.position
        if not symbol.isGlobal:
            temporaryPosition=generator.addNewTemporary()
            generator.addNewExpression(temporaryPosition, 'P', symbol.position, '+')
        if value.getType() == 'boolean':
            temporaryLabel = generator.addNewLabel()
            
            generator.defineLabel(value.labelTrue)
            generator.setStack(temporaryPosition, "1")
            
            generator.addGotoLabel(temporaryLabel)

            generator.defineLabel(value.labelFalse)
            generator.setStack(temporaryPosition, "0")

            generator.defineLabel(temporaryLabel)
        else:
            generator.setStack(temporaryPosition,value.getValue())
        generator.addNewComment('End variable declaration')
        
    