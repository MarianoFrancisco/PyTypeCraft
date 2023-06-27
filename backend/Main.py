# CORS -> Cross Origin Resource Sharing
# Si no existe el CORS, no se puede acceder a los recursos de un servidor desde otro servidor
from Parser import parse as Parser
from Parser import add_natives as Natives
from src.Semantic.tree import Tree_
from src.Semantic.exception import CompilerException
from src.Semantic.symbol_table import SymbolTable
from src.Instruction.function import Function
from Lexer import errors, tokens, lexer
from flask import Flask, request
import json
from flask_cors import CORS
from flask.helpers import url_for
from werkzeug.utils import redirect
from typing import Dict, List
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
    Table = {}
    instructions = Parser(valueTemporary)
    ast = Tree_(instructions)
    globalScope = SymbolTable()
    ast.setGlobalScope(globalScope)
    Natives(ast)
    for error in errors:
        ast.setExceptions(error)
    try:
        for instruction in ast.getInstr():     
            if isinstance(instruction, Function):
                ast.setFunctions(instruction)
        for instruction in ast.getInstr():
            if not(isinstance(instruction, Function)):
                value = instruction.execute(ast, globalScope)
                if isinstance(value, CompilerException):
                    ast.setExceptions(value)
    except:
        CompilerException("Structure","No has ingresado nada",0,0)
    Exceptions = ast.getExceptions()
    print(Exceptions)
    global Simbolos
    Simbolos = ast.getGlobalScope().table
    consola = ast.getConsole()
    return json.dumps(consola)


@app.route('/mistake')
def getMistake():
    global Exceptions
    value= []
    for exception in Exceptions:
        value.append(exception.toStringData())
    
    return {'valores': value}

# @app.route('/symbol')
# def getTabla():
#     global Simbolos
#     Dic = []
#     for x in Simbolos:
#         aux = Simbolos[x].getValor()
#         tipo = Simbolos[x].getTipo()
#         tipo = getTipo(tipo)
#         fila = Simbolos[x].getFila()
#         colum = Simbolos[x].getColum()
#         if isinstance(aux, List):
#             aux = getValores(aux)
#             a = []
#             a.append(str(x))
#             a.append(str(aux))
#             a.append('Array')
#             a.append('Global')
#             a.append(str(fila))
#             a.append(str(colum))
#             Dic.append(a)
#         elif isinstance(aux, Dict):
#             aux = getValores2(aux)
#             a = []
#             a.append(str(x))
#             a.append(str(aux))
#             a.append('Struct')
#             a.append('Global')
#             a.append(str(fila))
#             a.append(str(colum))
#             Dic.append(a)
#         else:
#             a = []
#             a.append(str(x))
#             a.append(str(aux))
#             a.append(tipo)
#             a.append('Global')
#             a.append(str(fila))
#             a.append(str(colum))
#             Dic.append(a)
#     return {'valores':Dic}

# def getValores(anterior):
#     actual = []
#     for x in anterior:
#         a = x.getValor()
#         if isinstance(a, List):
#             value = getValores(a)
#             actual.append(value)
#         elif isinstance(a, Dict):
#             value = getValores2(a)
#             actual.append(value)
#         else:
#             actual.append(x.getValor())
#     return actual

# def getValores2( dict):
#     val = "("
#     for x in dict:
#         a = dict[x].getValor()
#         if isinstance(a, List):
#             value = getValores(a)
#             val += str(value) + ", "
#         elif isinstance(a, Dict):
#             value = getValores2(a)
#             val += str(value) + ", "
#         else:
#             val += str(dict[x].getValor()) + ", "
#     val = val[:-2]  
#     val += ")"
#     return val

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug = False, port=4000)