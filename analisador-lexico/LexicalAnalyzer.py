import sys

class Token:
    def __init__(self, word, lex, line):
        self.word = word
        self.lex = lex
        self.line = line

    def __str__(self):
        return self.word+"\t"+self.lex+"\t"+str(self.line)


class LexicalAnalyzer:
    def __init__(self):
        self.key_words = ["program", "var", "integer", "real", "boolean", "procedure", "begin","end", "if", "then", "else", "while", "do", "not"]

    def analyze(self,program,i=0):
        line_count = 1
        token = ""
        tam = len(program)
        i = 0
        lex = ""
        result = []

        while i <= tam-1:

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
                    ######################## MODIFICAÇÃO ########################
                    elif program[i] == "i":
                        token += program[i]
                        i += 1
                        if program[i] in "+-":
                            token += program[i]
                            i+=1
                            if program[i].isdigit():
                                token += program[i]
                                i+=1
                                lex = "Número Complexo"
                                while i < tam-1:
                                    if program[i].isdigit():
                                        token += program[i]
                                        i+=1
                                    else:
                                        break
                            else:
                                token = token[:-2]
                                i -= 2
                                break
                        else:
                            token = token[:-1]
                            i -= 1
                            break
                    else:
                        break
                    ######################## MODIFICAÇÃO ########################
            elif program[i].isalpha():      #Verifica se o elemento é uma letra
                token += program[i]
                i+=1
                while i < tam-1:    #Procura por mais letras ou números ou _
                    if program[i].isalpha() or program[i].isdigit() or program[i] is "_":
                        token += program[i]
                        i+=1
                    else:
                        break

                if token in self.key_words:     #Verfica se é uma das palavras-chave
                    lex = "Palavra Reservada"
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

            elif program[i] is "<": #Verificar se são os operadores relacionais "<" ou "<=" ou "<>"
                token = "<"
                i+=1
                lex = "Operador Relacional"

                if program[i] in "=>":
                    token += program[i]
                    i+=1

            elif program[i] is ">":     #Verificar se são os operadores relacionais ">" ou ">="
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

            elif program[i] in "*":    #Verificar se são os operadores multiplicativos
                token = program[i]
                i+=1
                lex = "Operador Multiplicativo"
            ######################## MODIFICAÇÃO ########################
            elif program[i] is "/":
                token = program[i]
                i+=1
                lex = "Operador Multiplicativo"

                if program[i] is "/":
                    i+=1
                    while i < tam-1:
                        if program[i] is "\n":
                            i+=1
                            line_count += 1
                            break
                        i+=1
                    continue
            ######################## MODIFICAÇÃO ########################
            elif program[i] is "{":     #Verificar se é início de comentário
                ln = line_count
                while i < tam -1:
                    i+=1
                    if program[i] is "}":   #Verificar se é fim de comentário
                        i+=1
                        break
                    elif program[i] is "\n":
                        line_count += 1

                else:
                    if program[-1] != "}":
                        sys.exit("ERRO Léxico: Comentário aberto e não fechado. Linha: "+str(ln))
                        break
                continue

            elif program[i] is "}":
                sys.exit("ERRO Léxico: Token '}' inesperado. Linha: "+str(line_count))
                break

            elif program[i] == "\n":    #Contagem das linhas
                line_count += 1
                i+=1
                continue

            elif program[i].isspace():       #Ignorar qualquer outra caracter de espaço
                i+=1
                continue

            else:   #Caso seja um character não aceito pela linguagem
                sys.exit("ERRO Léxico: Token '"+program[i]+"' não aceito. Linha: "+str(line_count))
                break

            #result.append([token,lex,line_count])
            result.append(Token(token,lex,line_count))
            token = ""

        return result


if __name__ == "__main__":
     with open(sys.argv[1],"r") as program:
         for ln in LexicalAnalyzer().analyze(program.read()):
             print (ln)