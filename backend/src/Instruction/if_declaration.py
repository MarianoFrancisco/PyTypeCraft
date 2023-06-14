from ..Abstract.abstract import Abstract
from ..Tabla_Simbolos.excepcion import Excepcion
from ..Tabla_Simbolos.tabla_simbolos import TablaSimbolos

class If(Abstract):

    def __init__(self, condition, ifBlock, elseBlock, elseIfBlock, line, column):
        self.condition = condition
        self.ifBlock = ifBlock
        self.elseBlock = elseBlock
        self.elseIfBlock = elseIfBlock
        super().__init__(line, column)
    

    def interpretar(self, arbol, tabla):
        condition = self.condition.interpretar(arbol, tabla)
        if isinstance(condition, Excepcion): return condition
        # Validar que el tipo sea booleano
        if bool(condition) == True:
            entorno = TablaSimbolos(tabla)  #NUEVO ENTORNO - HIJO - Vacio
            for instruccion in self.ifBlock:
                result = instruccion.interpretar(arbol, entorno) 
                if isinstance(result, Excepcion) :
                    arbol.setExcepciones(result)
        elif self.elseBlock != None:
            entorno = TablaSimbolos(tabla)
            for instruccion in self.elseBlock:
                result = instruccion.interpretar(arbol, entorno) 
                if isinstance(result, Excepcion) :
                    arbol.setExcepcion(result)
        elif self.elseIfBlock != None:
            result = self.elseIfBlock.interpretar(arbol, tabla)
