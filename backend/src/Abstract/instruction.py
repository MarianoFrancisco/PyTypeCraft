from abc import ABC, abstractmethod


class Instruction(ABC):

    def __init__(self, line, column):
        self.line = line
        self.column = column

    @abstractmethod
    def execute(self, tree, table):
        pass