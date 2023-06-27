# CORS -> Cross Origin Resource Sharing
# Si no existe el CORS, no se puede acceder a los recursos de un servidor desde otro servidor
from Parser import parse as Parser
from Parser import add_natives as Natives
from Parser import add_structs as Structs
from src.Semantic.tree import Tree_
from src.Semantic.exception import CompilerException
from src.Semantic.symbol_table import SymbolTable
from src.Instruction.function import Function
from src.Instruction.struct import Struct
from Lexer import errors, tokens, lexer
from flask import Flask, request
import json
from flask_cors import CORS
from flask.helpers import url_for
from werkzeug.utils import redirect
from typing import Dict, List
from graphviz import Graph
import sys
sys.setrecursionlimit(10000000)

app = Flask(__name__)
CORS(app)

@app.route('/', methods = ["GET"])
def saludo():
    return {"mensaje": "Hola mundo!"}

@app.route('/compile', methods = ["POST","GET"])
def compilar():
    if request.method == "POST":
        entrada = request.data.decode("utf-8")
        entrada = json.loads(entrada)
        global valueTemporary
        valueTemporary = entrada["code"]
        return redirect(url_for("output"))
    else:
        return {"mensaje": "No compilado"}

@app.route('/output')
def output():
    global valueTemporary
    global Exceptions
    global Table
    global ast
    Table = {}
    instructions = Parser(valueTemporary)
    ast = Tree_(instructions)
    globalScope = SymbolTable()
    ast.setGlobalScope(globalScope)
    Natives(ast)
    Structs(ast)
    for error in errors:
        ast.setExceptions(error)
    try:
        for instruction in ast.getInstr():     
            if isinstance(instruction, Struct):
                ast.addInterface(instruction)
            if isinstance(instruction, Function):
                ast.setFunctions(instruction)
        for instruction in ast.getInstr():
            if not(isinstance(instruction, Function)):
                value = instruction.execute(ast, globalScope)
                if isinstance(value, CompilerException):
                    ast.setExceptions(value)
    except:
        ast.setExceptions(CompilerException("Structure","No has ingresado nada",0,0))
    Exceptions = ast.getExceptions()
    global Symbols
    Symbols = ast.getGlobalScope().getGlobalScope()
    consola = ast.getConsole()
    return json.dumps(consola)


@app.route('/mistake')
def getMistake():
    global Exceptions
    value= []
    for exception in Exceptions:
        value.append(exception.toStringData())
    return {'valores': value}

@app.route('/plot')
def getAstPlot():
    global ast
    try:
        if len(ast.getExceptions()) > 0: return {"error" : "Existen errores en el codigo, no se puede generar el arbol"}
        dot = Graph(filename='./static/process.gv')
        dot.attr(splines='false')
        dot.node_attr.update(shape='circle', fontname='arial',
                             color='blue4', fontcolor='blue4')
        dot.edge_attr.update(color='blue4')
        for instruccion in ast.getInstr():
            if not(isinstance(instruccion, Function)):
                instruccion.plot(dot)

        dot.render(filename='./static/process.gv', format='png')
    except:
        return {"error": "No se ha analizado el codigo"}

    else:
        # EN ESTA PARTE SE RETORNA LA URL CON EL PDF DEL ARBOL GENERADO, CAMBIAR EL DOMINIO DE SER NECESARIO
        return {'url': 'http://localhost:4000/static/process.gv.png'}
    

@app.route('/symbol')
def getTable():
    global Symbols
    Dic = []
    for symbol in Symbols:
        value = Symbols[symbol].getValue()
        type = Symbols[symbol].getType()
        line = Symbols[symbol].line
        column = Symbols[symbol].column
        if isinstance(value, List):
            value = getValueData(value)
            saveSymbol = []
            saveSymbol.append(str(symbol))
            saveSymbol.append(str(value))
            saveSymbol.append('Array')
            saveSymbol.append('Global')
            saveSymbol.append(str(line))
            saveSymbol.append(str(column))
            Dic.append(saveSymbol)
        elif isinstance(value, Dict):
            value = getValueDataSecond(value)
            saveSymbol = []
            saveSymbol.append(str(symbol))
            saveSymbol.append(str(value))
            saveSymbol.append('Struct')
            saveSymbol.append('Global')
            saveSymbol.append(str(line))
            saveSymbol.append(str(column))
            Dic.append(saveSymbol)
        else:
            saveSymbol = []
            saveSymbol.append(str(symbol))
            saveSymbol.append(str(value))
            saveSymbol.append(type)
            saveSymbol.append('Global')
            saveSymbol.append(str(line))
            saveSymbol.append(str(column))
            Dic.append(saveSymbol)
    return {'valores':Dic}

def getValueData(previous):
    current = []
    for value in previous:
        data = value.getValor()
        if isinstance(data, List):
            value = getValueData(data)
            current.append(value)
        elif isinstance(data, Dict):
            value = getValueDataSecond(data)
            current.append(value)
        else:
            current.append(value.getValue())
    return current

def getValueDataSecond( dict):
    val = "("
    for value in dict:
        data = dict[value].getValor()
        if isinstance(data, List):
            value = getValueData(data)
            val += str(value) + ", "
        elif isinstance(data, Dict):
            value = getValueDataSecond(data)
            val += str(value) + ", "
        else:
            val += str(dict[value].getValue()) + ", "
    val = val[:-2]  
    val += ")"
    return val

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug = False, port=4000)
