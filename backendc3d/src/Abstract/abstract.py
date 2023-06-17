from abc import ABC, abstractmethod


class Abstract(ABC):

    def __init__(self, line, column):
        self.line = line
        self.column = column
        self.labelTrue=''
        self.labelFalse=''

    @abstractmethod
    def execute(self, tree, table):
        pass
    
    ''' Getter & setters label true & false'''
    def getLabelTrue(self):
        return self.labelTrue
    def setLabelTrue(self,newLabelTrue):
        self.labelTrue=newLabelTrue

    def getLabelFalse(self):
        return self.labelFalse
    def setLabelFalse(self,newLabelFalse):
        self.labelFalse=newLabelFalse