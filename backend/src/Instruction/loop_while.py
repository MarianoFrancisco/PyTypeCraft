from ..Instruction.reserved_break import ReservedBreak
from ..Instruction.reserved_continue import ReservedContinue
from ..Instruction.reserved_return import ReservedReturn
from ..Semantic.symbol_table import SymbolTable
from ..Semantic.exception import CompilerException
from ..Abstract.abstract import Abstract
import uuid

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

    def plot(self, root):
        node_id = str(uuid.uuid4())
        root.node(node_id, "While")

        # Create node for condition
        condition_id = self.condition.plot(root)
        root.edge(node_id, condition_id)

        # Create node for instructions
        if self.instructions:
            instructions_id = str(uuid.uuid4())
            root.node(instructions_id, "Instructions")
            root.edge(node_id, instructions_id)

            # Create nodes for each instruction and connect them to the instructions node
            for instruction in self.instructions:
                instruction_node_id = instruction.plot(root)
                root.edge(instructions_id, instruction_node_id)

        return node_id