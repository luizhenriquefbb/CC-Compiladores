
import sys,os

sys.path.append("/".join(os.getcwd().split("/")[:-1])+"/analisador-lexico")

import LexicalAnalyzer

class SyntaxAnalyzer():
    def __init__(self, list_tokens):
        self.list_tokens = list_tokens
        self.current =  None
        self.index = 0

    def next(self):
        if self.index < len(self.list_tokens):
            self.current = self.list_tokens[self.index]
            print (self.current)
            self.index += 1
            return self.current

        sys.exit("Erro: O programa terminou, mas a análise não")
        return None

    def startAnalysis(self):
        if self.next().word == "program":
            if self.next().lex == "Identificador":
                if self.next().word == ";":
                    self.declaracoes_variaveis()
                    self.declaracoes_subprogramas()
                    self.comando_composto()
                    if self.next().word == ".":
                        return True
                    else:
                        sys.exit("Erro: Fata o '.' no fim do programa")
                else:
                   sys.exit("Erro: Falta o ';' após o nome do programa")
            else:
                sys.exit("Erro: O programa está sem nome")
        else:
            sys.exit("Erro: O programa não começou com 'program'")

    def declaracoes_variaveis(self):
        if self.next().word == "var":
            self.lista_declaracoes_variaveis()
        else:
            self.index -= 1

    def lista_declaracoes_variaveis(self):
        if self.lista_de_identificadores():
            if self.next().word == ":":
                self.tipo()
                if self.next().word == ";":
                    self.lista_declaracoes_variaveis_ln()
                else:
                    sys.exit("O ';' não enontrado")
            else:
                sys.exit("O ':' não foi encontrado")
        else:
            sys.exit("Era esperado um identificador")

    def lista_declaracoes_variaveis_ln(self):
        if self.lista_de_identificadores():
            if self.next().word == ":":
                self.tipo()
                if self.next().word == ";":
                    self.lista_declaracoes_variaveis_ln()
                else:
                    sys.exit("O ';' não enontrado")
            else:
                sys.exit("O ':' não foi encontrado")

    def lista_de_identificadores(self):
        if self.next().lex == "Identificador":
            self.lista_de_identificadores_ln()
            return True
        else:
            self.index -= 1
            return False

    def lista_de_identificadores_ln(self):
        if self.next().word == ",":
            if self.next().lex == "Identificador":
                self.lista_de_identificadores_ln()
            else:
                sys.exit("Era esperado um identificador")
        else:
            self.index -= 1

    def tipo(self):
        if self.next().word in ["integer","real","boolean"]:
            pass
        else:
            sys.exit("Não é um tipo")

    def declaracoes_subprogramas(self):
        self.declaracoes_subprogramas_ln()

    def declaracoes_subprogramas_ln(self):
        if self.declaracao_subprograma():
            if self.next().word == ";":
                self.declaracoes_subprogramas_ln()
            else:
                sys.exit("Declaração de subprograma sem ';'")

    def declaracao_subprograma(self):
        if self.next().word == "procedure":
            if self.next().lex == "Identificador":
                self.argumentos()
                if self.next().word == ";":
                    self.declaracoes_variaveis()
                    self.declaracoes_subprogramas()
                    self.comando_composto()
                    return True
                else:
                    sys.exit("O ';' era esperado, mas não foi encontrador")
            else:
                sys.exit("Procedure sem identificador")
        else:
            self.index -= 1
            return False

    def argumentos(self):
        if self.next().word == "(":
            self.lista_de_parametros()
            if self.next().word == ")":
                pass
            else:
                sys.exit("Era esperado um ')'")
        else:
            self.index -= 1

    def lista_de_parametros(self):
        self.lista_de_identificadores()
        if self.next().word == ":":
            self.tipo()
            self.lista_de_parametros_ln()
        else:
            sys.exit("O ':' era esperado")

    def lista_de_parametros_ln(self):
        if self.next().word == ";":
            self.lista_de_identificadores()
            if self.next().word == ":":
                self.tipo()
                self.lista_de_parametros_ln()
            else:
                sys.exit("Era esparado ':'")
        else:
            self.index -= 1

    def comando_composto(self):
        if self.next().word == "begin":
            self.comandos_opcionais()
            if self.next().word == "end":
                return True
            else:
                sys.exit("Comando 'end' não encontrado")
        else:
            self.index -= 1
            return False

    def comandos_opcionais(self):
        self.lista_de_comandos()

    def lista_de_comandos(self):
        self.comando()
        self.lista_de_comandos_ln()


    def lista_de_comandos_ln(self):
        if self.next().word == ";":
            self.comando()
            self.lista_de_comandos_ln()
        else:
            self.index -= 1

    def comando(self):
        if self.variavel():
            if self.next().word == ":=":
                self.expressao()
                return
            else:
                sys.exit("O ':=' era esperado")

        elif self.ativacao_de_procedimento():
            pass

        elif self.comando_composto():
            pass

        elif self.next().word == "if":
            self.expressao()
            if self.next().word == "then":
                self.comando()
                self.parte_else()
                return
            else:
                sys.exit("O 'then' era eperado")
        else:
            self.index -= 1

        if self.next().word == "while":
            self.expressao()
            if self.next().word == "do":
                self.comando()
            else:
                sys.exit("Era esperado um 'do'")
        else:
            self.index -= 1

    def parte_else(self):
        if self.next().word == "else":
            self.comando()
        else:
            self.index -= 1

    def variavel(self):
        if self.next().lex == "Identificador":
            return True
        else:
            self.index -= 1
            return False

    def ativacao_de_procedimento(self):
        if self.next().lex == "Identificador":
            if self.next().word == "(":
                self.lista_de_expressoes()
                if self.next().word == ")":
                    return True
                else:
                    sys.exit("O ')' era esperado")
            else:
                self.index -= 1
                return True
        else:
            self.index -= 1
            return False

    def lista_de_expressoes(self):
        self.expressao()
        self.lista_de_expressoes_ln()

    def lista_de_expressoes_ln(self):
        if self.next().word == ",":
            self.expressao()
            self.lista_de_expressoes_ln()
        else:
            self.index -= 1

    def expressao(self):
        self.expressao_simples()
        if self.op_relacional():
            self.expressao_simples()

    def expressao_simples(self):
        if self.termo():
            self.expressao_simples_ln()
        elif self.sinal():
            self.termo()
            self.expressao_simples_ln()
        else:
            sys.exit("Uma expressão era esperada")

    def expressao_simples_ln(self):
        if self.op_aditivo():
            self.termo()
            self.expressao_simples_ln()

    def termo(self):
        if self.fator():
            self.termo_ln()
            return True
        else:
            #sys.exit("Era esperado um fator")
            return False

    def termo_ln(self):
        if self.op_multiplicativo():
            self.fator()
            self.termo_ln()

    def fator(self):
        token = self.next()
        if token.lex == "Identificador":
            if self.next().word == "(":
                self.lista_de_expressoes()
                if self.next().word == ")":
                    pass
                else:
                    sys.exit("Era esperado um ')'")
            else:
                self.index -= 1
                return True
        elif token.lex in ["Número Inteiro","Número Real"]:
            pass
        elif token.word in ["true","false"]:
            pass
        elif token.word == "(":
            self.expressao()
            if self.next().word == ")":
                pass
            else:
                sys.exit("Falta o ')'")
        elif token.word == "not":
            self.fator()
        else:
            self.index -= 1
            return False

        return True

    def sinal(self):
        if self.next().word in "+-":
            return True
        else:
            self.index -= 1
            return False

    def op_relacional(self):
        if self.next().word in ["=","<",">","<=",">=","<>"]:
            return True
        else:
            self.index -= 1
            return False

    def op_aditivo(self):
        if self.next().word in ["+","-","or"]:
            return True
        else:
            self.index -= 1
            return False

    def op_multiplicativo(self):
        if self.next().word in ["*","/","and"]:
            return True
        else:
            self.index -= 1
            return False

############################

if __name__ == "__main__":
     with open(sys.argv[1],"r") as program:
        lex = LexicalAnalyzer.LexicalAnalyzer()
        syn = SyntaxAnalyzer(lex.analyze(program.read()))
        if (syn.startAnalysis()):
            print("PROGRAMA OK!")
