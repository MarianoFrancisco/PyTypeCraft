from abc import ABC, abstractmethod


class Abstract(ABC):

    def __init__(self, line, column):
        self.line = line
        self.column = column

    @abstractmethod
    def interpret(self, tree, table):
        pass
