from sintatico import sintatico
from util import *
from lexico import lexico


if __name__ == '__main__':
    # input_string = 'if \n43teste var \n uo{qweh 322}23 j23jn234 program'
    input_string = (
        "program id; {programa exemplo}\n"+
        "var\n"+
        "valor1: integer;\n"+
        "valor2: real;\n"+
        "begin\n"+
        "valor1 := 10 *;\n"+
        "end.\n"+
        "90 89.7 12   & = #\n"+
        "variavel var1\n"+
        "// isso eh um comentario de linha\n"+
        "0.3x2.0y4.9z"+
        "12.34.56"+
        "")

    print_row("TOKEN", "CLASSIFICACAO", "LINHA")
    sintatico(input_string)
    lexico()

    print("the end")