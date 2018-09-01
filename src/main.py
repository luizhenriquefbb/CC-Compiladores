from sintatico import sintatico
from util import *
from lexico import lexico


if __name__ == '__main__':
 
    input_string = open("programas/teste.txt", "r").read()

    print_row("TOKEN", "CLASSIFICACAO", "LINHA")
    sintatico(input_string)
    if lexico() == True:
        print("sucess")
    else:
        print("fail")

    print("the end")