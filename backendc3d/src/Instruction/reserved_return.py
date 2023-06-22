from ..Abstract.abstract import Abstract
from ..Semantic.exception import CompilerException

class ReservedReturn(Abstract):

    def __init__(self,expression, line,column):
        self.expression = expression
        self.value = None
        self.type = None
        self.labelTrue = ''
        self.labelFalse = ''
        super().__init__(line,column)
    
    def execute(self, tree,table):
        resultExpression = self.expression.execute(tree, table)
        if isinstance(resultExpression, CompilerException): return resultExpression
        self.type = resultExpression.getType()
        self.value = resultExpression.getValue()
        if self.type == 'boolean':
            self.labelTrue = resultExpression.getLabelTrue()
            self.labelFalse = resultExpression.getLabelFalse()
        return self
    '''Getter & setters'''
    def getValue(self):
        return self.value
    def setValue(self, value):
        self.value = value

    def getType(self):
        return self.type
    def setType(self, type):
        self.type  = type

    def getLabelTrue(self):
        return self.labelTrue
    def setLabelTrue(self, labelTrue):
        self.labelTrue = labelTrue

    def getLabelFalse(self):
        return self.labelFalse
    def setLabelFalse(self, labelFalse):
        self.labelFalse = labelFalse
   
    
    
    
    
    