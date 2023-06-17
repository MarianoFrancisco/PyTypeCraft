from ..Abstract.abstract import Abstract
from ..Semantic.exception import CompilerException


class Concat(Abstract):

    def __init__(self, parameters, line, column):
        self.parameters = parameters
        super().__init__(line, column)

    def execute(self, tree, table):
        if len(self.parameters)<2:
            return CompilerException("Semantico", "Concat requiere al menos dos array", self.line, self.column)
        #first_array=table.getSymbolById(self.parameters[0].id)
        concat_array=[]
        for parameter in self.parameters:
            plus_parameter=parameter.execute(tree,table)
            concat_array+=plus_parameter
        #first_array.value=concat_array
        #return first_array.value
        return concat_array
