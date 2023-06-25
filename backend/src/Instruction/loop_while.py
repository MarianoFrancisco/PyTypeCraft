from ..Instruction.reserved_break import ReservedBreak
from ..Instruction.reserved_continue import ReservedContinue
from ..Instruction.reserved_return import ReservedReturn
from ..Semantic.symbol_table import SymbolTable
from ..Semantic.exception import CompilerException
from ..Abstract.abstract import Abstract


class While(Abstract):

    def __init__(self, condition, instructions, line, column):
        self.condition = condition
        self.instructions = instructions
        self.line = line
        self.colum = column

    def execute(self, tree, table):
        while True:
            condition = self.condition.execute(tree, table)

            if isinstance(condition, CompilerException):
                return condition

            if self.condition.type != 'boolean':
                return CompilerException("Semantico", "Condicion no valida en el While", self.line, self.column)

            if bool(condition):
                for instruction in self.instructions:
                    scope = SymbolTable(table)
                    value = instruction.execute(tree, scope)

                    if isinstance(value, CompilerException):
                        tree.setExceptions(value)
                        return value

                    if isinstance(value, ReservedBreak):
                        return None

                    if isinstance(value, ReservedReturn):
                        return value

                    if isinstance(value, ReservedContinue):
                        break
            else:
                break
