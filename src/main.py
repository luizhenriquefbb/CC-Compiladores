# from sintatico import sintatico
from util import *
from sintatico import sintatico
from lexico_v2 import LexicalAnalyzer


if __name__ == '__main__':
 
    # input_string = open("programas/teste.txt", "r").read()
    # input_string = open("programas/mod.txt", "r").read()
    # input_string = open("programas/prog2.txt", "r").read()
    # input_string = open("programas/do_while_test.txt", "r").read()
    # input_string = open("programas/aula.txt", "r").read()
    input_string = open("programas/programa.txt", "r").read()

    # run lexical
    lexical_output = LexicalAnalyzer().analyze(input_string)
    print_row("TOKEN", "CLASSIFICACAO", "LINHA")
    for el in lexical_output:
        print (el)
    
    # adpter
    sint_input = []
    for el in lexical_output:
        sint_input.append({"token": el.word, "classification": el.lex, "line":el.line})
    
    # run sintati.
    sint_output = sintatico(sint_input)
    
    if sint_output == True:
        print("\nsucess")
    else:
        print("\nfail")

    print("the end")