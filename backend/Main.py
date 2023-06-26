# CORS -> Cross Origin Resource Sharing
# Si no existe el CORS, no se puede acceder a los recursos de un servidor desde otro servidor
from Parser import parse as Parser
from src.Semantic.tree import Tree_
from src.Semantic.exception import CompilerException
from src.Semantic.symbol_table import SymbolTable
from Lexer import errors, tokens, lexer
from flask import Flask, request
import json
from flask_cors import CORS
from flask.helpers import url_for
from werkzeug.utils import redirect

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
        print(entrada)
        global tmp_val
        tmp_val = entrada["code"]
        return redirect(url_for("output"))
    else:
        return {"mensaje": "No compilado"}

@app.route('/output')
def output():
    global tmp_val
    global Tabla
    Tabla = {}
    instrucciones = Parser(tmp_val)
    ast = Tree_(instrucciones)
    TsgGlobal = SymbolTable()
    ast.setGlobalScope(TsgGlobal)
    for error in errors:
        ast.setExceptions(error)

    for instruccion in ast.getInstr():
        value = instruccion.execute(ast, TsgGlobal)
        if isinstance(value, CompilerException):
            ast.setExceptions(value)

    global Simbolos
    Simbolos = ast.getGlobalScope().table
    consola = str(ast.getConsole())
    print('Consola: ', consola)
    return json.dumps({'consola':consola, 'mensaje': 'Compilado :3'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug = False, port=4000)