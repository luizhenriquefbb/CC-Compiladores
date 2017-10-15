import sys

from analisadorLexico import LexicalAnalyzer
from analisadorSintaticoSemantico import SyntaxAnalyzer


with open(sys.argv[1],"r") as program:
        lex = LexicalAnalyzer()
        syn = SyntaxAnalyzer(lex.analyze(program.read()))
        if (syn.startAnalysis()):
            print("PROGRAMA OK!")