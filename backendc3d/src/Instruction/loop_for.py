from ..Semantic.symbol import Symbol
from ..Semantic.exception import CompilerException
from ..Abstract.abstract import Abstract
from ..Semantic.symbol_table import SymbolTable
from ..Semantic.c3d_generator import C3DGenerator

class For(Abstract):

    def __init__(self, requirement, restriction, variation, instruction, line,column):
        self.requirement = requirement
        self.restriction = restriction
        self.variation = variation
        self.instruction = instruction
        super().__init__(line,column)
    
    def execute(self, tree, table):
        callGenerator=C3DGenerator()
        generator=callGenerator.getGenerator()
        generator.addNewComment('Start loop for')
        flag = True
        entorn = table
        if table.searchSymbolById(self.requirement.id):#search for the first declaration
            flag = False#search if exist id

        
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
            


