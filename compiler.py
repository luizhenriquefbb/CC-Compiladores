#!/usr/bin/python3

import sys

from analisadorLexico import LexicalAnalyzer
from analisadorSintaticoSemantico import SyntaxSemanticAnalyzer


with open(sys.argv[1],"r") as program:
        lex = LexicalAnalyzer()
        syn = SyntaxSemanticAnalyzer(lex.analyze(program.read()))
        if (syn.startAnalysis()):
            print("PROGRAMA OK!")