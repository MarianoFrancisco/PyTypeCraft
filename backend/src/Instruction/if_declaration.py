from ..Instruction.reserved_break import ReservedBreak
from ..Instruction.reserved_continue import ReservedContinue
from ..Semantic.exception import CompilerException
from ..Semantic.symbol_table import SymbolTable
from ..Abstract.abstract import Abstract
from ..Instruction.reserved_return import ReservedReturn
import uuid
class IfSentence(Abstract):

    def __init__(self, condition, ifBlock, elseBlock, elseIfBlock, line, column):
        super().__init__(line, column)
        self.condition = condition
        self.ifBlock = ifBlock
        self.elseBlock = elseBlock
        self.elseIfBlock = elseIfBlock
    

    def execute(self, tree, table):
        conditionEvaluated = self.condition.execute(tree, table)
        if isinstance(conditionEvaluated, CompilerException): return conditionEvaluated
        # Validar que el tipo sea booleano
        if bool(conditionEvaluated) == True:
            scope = SymbolTable(table)  #NUEVO ENTORNO - HIJO - Vacio
            for instruccion in self.ifBlock:
                result = instruccion.execute(tree, scope) 
                if isinstance(result, CompilerException) :
                    tree.setExceptions(result)
                if isinstance(result, ReservedReturn): return result
                if isinstance(result, ReservedBreak): return result
                if isinstance(result, ReservedContinue): return result
        elif self.elseBlock != None:
            scope = SymbolTable(table)
            for instruccion in self.elseBlock:
                result = instruccion.execute(tree, scope) 
                if isinstance(result, CompilerException) :
                    tree.setExceptions(result)
                if isinstance(result, ReservedReturn): return result
                if isinstance(result, ReservedBreak): return result
                if isinstance(result, ReservedContinue): return result
        elif self.elseIfBlock != None:
            result = self.elseIfBlock.execute(tree, table)
            if isinstance(result, ReservedReturn): return result
            if isinstance(result, ReservedBreak): return result
            if isinstance(result, ReservedContinue): return result

    def plot(self, root):
        node_id = str(uuid.uuid4())
        root.node(node_id, "If Sentence")

        # Create node for condition
        condition_node_id = self.condition.plot(root)

        # Create edges from the root node to the condition node
        root.edge(node_id, condition_node_id)

        # Check if there is an ifBlock and create nodes for its instructions
        if self.ifBlock:
            if_block_node_id = str(uuid.uuid4())
            root.node(if_block_node_id, "If Block")
            root.edge(node_id, if_block_node_id)

            # Create nodes for each instruction in the ifBlock
            for instruction in self.ifBlock:
                instruction_node_id = instruction.plot(root)
                root.edge(if_block_node_id, instruction_node_id)

        # Check if there is an elseBlock and create nodes for its instructions
        if self.elseBlock:
            else_block_node_id = str(uuid.uuid4())
            root.node(else_block_node_id, "Else Block")
            root.edge(node_id, else_block_node_id)

            # Create nodes for each instruction in the elseBlock
            for instruction in self.elseBlock:
                instruction_node_id = instruction.plot(root)
                root.edge(else_block_node_id, instruction_node_id)

        # Check if there is an elseIfBlock and create node for it
        if self.elseIfBlock:
            else_if_block_node_id = self.elseIfBlock.plot(root)
            root.edge(node_id, else_if_block_node_id)

        return node_id