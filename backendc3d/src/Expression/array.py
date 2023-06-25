#from ..Semantic.c3d_generator import C3DGenerator
from ..Semantic.exception import CompilerException
from ..Abstract.abstract import Abstract


class Array(Abstract):
    def __init__(self, expressions, line, column):
        super().__init__(line, column)
        self.expressions = expressions
        self.type = None

    def execute(self, tree, table):
        #callGenerator=C3DGenerator()
        #generator=callGenerator.getGenerator()
        #generator.addNewComment("Start array")
        arr = []
        for value in self.expressions:
            result = value.execute(tree, table)
            if isinstance(result, CompilerException): return result
            if self.type != None and self.type != value.type:
                self.type = 'any'
            else:
                self.type = value.type
            arr.append(result)
        return arr
        """  generator.fboundError()
        temp = generator.addTemp()
        tempPos = var.pos
        if not var.isGlobal:
            tempPos = generator.addTemp()
            generator.addExp(tempPos, 'P', var.pos, "+")
        generator.getStack(temp, tempPos)
        x = 0
        tipo = var.getTipo()
        tipoAux = var.getTipoAux()
        for value in self.indice:
            x += 1
            tmp3 = generator.addTemp()
            tmp4 = generator.addTemp()
            tmp5 = generator.addTemp()
            Lbl1 = generator.newLabel()
            Lbl2 = generator.newLabel()
            Lbl3 = generator.newLabel()

            indice = value.interpretar(arbol, tabla)
            generator.addExp(tmp3, temp, indice.getValue(), "+")

            generator.addIf(indice.getValue(),'1','<',Lbl1) #Agregado
            generator.getHeap(tmp5, temp)
            generator.addIf(indice.getValue(),tmp5,'>', Lbl1) #Agregado
            generator.addGoto(Lbl2)
            generator.putLabel(Lbl1)
            generator.callFun('BoundsError')
            generator.addGoto(Lbl3)
            generator.putLabel(Lbl2)

            generator.getHeap(tmp4, tmp3)

            generator.addGoto(Lbl3)
            generator.putLabel(Lbl3)

            temp = tmp4
            if x == len(self.indice):
                var.setTipo(var.getTipoAux())
            else:
                if isinstance(var.getTipoAux(), List):
                    var.setTipo(var.getTipoAux()[0])
                    var.setTipoAux(var.getTipoAux()[1])
                else:
                    return Excepcion("Semantico", "No se puede acceder al arreglo", self.fila, self.colum)
        generator.addComment(f'Fin compilacion de acceso de la variable {self.id}')
        space = Return(tmp4, var.getTipo(), True, var.getTipoAux())
        var.setTipo(tipo)
        var.setTipoAux(tipoAux)
        generator.addNewComment("End array")
        return space """
        # arr = []
        # for value in self.expressions:
        #     result = value.execute(tree, table)
        #     if isinstance(result, CompilerException): return result
        #     if self.type != None and self.type != value.type:
        #         self.type = 'any'
        #     else:
        #         self.type = value.type
        #     arr.append(result)
        # return arr
