import sys

class LexicalAnalyzer(object):
    """docstring for LexicalAnalyzer."""
    def __init__(self):
        self.key_words = ["program", "var", "integer", "real", "boolean", "procedure", "begin","end", "if", "then", "else", "while", "do", "not"]
    def analyze(self,program,i=0):
        line_count = 1
        token = ""
        tam = len(program)
        i = 0
        lex = ""
        result = []

        while i < tam-1:

            if program[i].isdigit():    #Se o elemento é um número
                token += program[i]
                i+=1
                lex = "Número Inteiro"
                while i < tam-1:    #Verificar se há mais números
                    if program[i].isdigit():
                        token += program[i]
                        i+=1
                    elif program[i] == ".":     #Se houver um . é pq é real
                        token += program[i]
                        i+=1
                        lex = "Número Real"
                        while i < tam - 1:  #Verificar se há mais números
                            if program[i].isdigit():
                                token += program[i]
                                i+=1
                            else:
                                break
                        break
                    else:
                        break

            elif program[i].isalpha():      #Verifica se o elemento é uma letra
                token += program[i]
                i+=1
                while i < tam-1:    #Procura por mais letras ou números
                    if program[i].isalpha() or program[i].isdigit():
                        token += program[i]
                        i+=1
                    else:
                        break

                if token in self.key_words:     #Verfica se é uma das palavras-chave
                    lex = "Palavra-chave"
                elif token is "or":     #Verificar se é o Operador "or"
                    lex = "Operador Aditivo"
                elif token is "and":    #Verificar se é o Operador "and"
                    lex = "Operador Multiplicativo"
                else:                   #Caso tudo contrário ele é um Identificador
                    lex = "Identificador"

            elif program[i] in ";.,()":     #Verificar se é um dos delimitadores
                token = program[i]
                lex = "Delimitador"
                i+=1

            elif program[i] is ":":     #Verificar se é o delimitador ":"  ou atribuição
                token = ":"
                i+=1
                lex = "Delimitador"

                if program[i] is "=":
                    token += "="
                    lex = "Atribuição"
                    i+=1

            elif program[i] is "=":     #Verificar se é o Operador Relacional "="
                token = "="
                i+=1
                lex = "Operador Relacional"

            elif program[i] is "<": #Verificar se são os operadores relacionais "<" ou "=>" ou "<>"
                token = "<"
                i+=1
                lex = "Operador Relacional"

                if program[i] in "=>":
                    token += program[i]
                    i+=1
            elif program[i] is ">":     #Verificar se são os operadores relacionais ">" ou ">=s"
                token = ">"
                i+=1
                lex = "Operador Relacional"

                if program[i] is "=":
                    token += "="
                    i+=1

            elif program[i] in "+-":    #Verificar se são os operadores aditivos
                token = program[i]
                i+=1
                lex = "Operador Aditivo"

            elif program[i] in "*/":    #Verificar se são os operadores multiplicativos
                token = program[i]
                i+=1
                lex = "Operador Multiplicativo"

            elif program[i] is "{":     #Verificar se é início de comentário
                while i < tam -1:
                    i+=1
                    if program[i] is "}":   #Verificar se é fim de comentário
                        break
                continue

            elif program[i] == "\n":    #Contagem das linhas
                line_count += 1
                i+=1
                continue
            else:       #Ignorar qualquer outra caracter
                i+=1
                continue

            result.append([token,lex,line_count])
            token = ""

        return result


if __name__ == "__main__":
     file_name = sys.argv[1]
     program = open(file_name,"r").read()

     for ln in LexicalAnalyzer().analyze(program):
         print (ln)
