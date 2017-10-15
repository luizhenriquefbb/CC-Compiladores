#!/usr/bin/python3
'''
Auth: Vinícius Matheus
Github: github.com/Vnicius
'''
import sys

from analisadorLexico import LexicalAnalyzer
from analisadorSintaticoSemantico import SyntaxSemanticAnalyzer


with open(sys.argv[1],"r") as program:
        lex = LexicalAnalyzer()
        syn = SyntaxSemanticAnalyzer(lex.analyze(program.read()))
        if (syn.startAnalysis()):
            print("PROGRAMA OK!")