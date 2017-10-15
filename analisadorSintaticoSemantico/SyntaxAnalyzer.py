
import sys,os

#sys.path.append("/".join(os.getcwd().split("/")[:-1])+"/analisador-lexico")

#import LexicalAnalyzer
from analisadorSintaticoSemantico import SymbolsTable
from analisadorSintaticoSemantico import TypesStack

class SyntaxAnalyzer():
    def __init__(self, list_tokens):
        self.list_tokens = list_tokens
        self.current =  None
        self.index = 0
        self.tabela = SymbolsTable()
        self.cont_begin_end = 0
        self.pilha_tipos = TypesStack()

    def next(self):
        if self.index < len(self.list_tokens):
            self.current = self.list_tokens[self.index]
            print (self.current)
            self.index += 1
            return self.current

        sys.exit("Erro: O programa terminou, mas a análise não")
        return None

    def verificar_id(self, token):
        if self.cont_begin_end:
            if not self.tabela.simbolo_na_tabela(token.word):
                sys.exit("O símbolo '"+ token.word +"' na linha "+ str(token.line) +" não foi declarado")
        else:
            self.tabela.push_simbolo(token.word, ".")

    def startAnalysis(self):
        if self.next().word == "program":
            self.tabela.novo_escopo()
            if self.next().lex == "Identificador":
                self.tabela.push_simbolo(self.current.word, "program")
                if self.next().word == ";":
                    self.declaracoes_variaveis()
                    self.declaracoes_subprogramas()
                    self.comando_composto()
                    if self.next().word == ".":
                        return True
                    else:
                        sys.exit("Erro: Fata o '.' no fim do programa. Linha: " + str(self.current.line))
                else:
                   sys.exit("Erro: Falta o ';' após o nome do programa. Linha: " + str(self.current.line))
            else:
                sys.exit("Erro: O programa está sem nome. Linha: " + str(self.current.line))
        else:
            sys.exit("Erro: O programa não começou com 'program'. Linha: " + str(self.current.line))

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
                    sys.exit("O ';' não enontrado. Linha: " + str(self.current.line))
            else:
                sys.exit("O ':' não foi encontrado. Linha: " + str(self.current.line))
        else:
            sys.exit("Era esperado um identificador. Linha: " + str(self.current.line))

    def lista_declaracoes_variaveis_ln(self):
        if self.lista_de_identificadores():
            if self.next().word == ":":
                self.tipo()
                if self.next().word == ";":
                    self.lista_declaracoes_variaveis_ln()
                else:
                    sys.exit("O ';' não enontrado. Linha: " + str(self.current.line))
            else:
                sys.exit("O ':' não foi encontrado. Linha: " + str(self.current.line))

    def lista_de_identificadores(self):
        if self.next().lex == "Identificador":

            self.verificar_id(self.current)
            
            self.lista_de_identificadores_ln()
            return True
        else:
            self.index -= 1
            return False

    def lista_de_identificadores_ln(self):
        if self.next().word == ",":
            if self.next().lex == "Identificador":

                self.verificar_id(self.current)

                self.lista_de_identificadores_ln()
            else:
                sys.exit("Era esperado um identificador. Linha: " + str(self.current.line))
        else:
            self.index -= 1

    def tipo(self):
        if self.next().word in ["integer","real","boolean"]:

            self.tabela.set_tipo(self.current.word)

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
                sys.exit("Declaração de subprograma sem ';'. Linha: " + str(self.current.line))

    def declaracao_subprograma(self):
        if self.next().word == "procedure":
            if self.next().lex == "Identificador":

                self.tabela.push_simbolo(self.current.word,"procedure")
                self.tabela.novo_escopo()

                self.argumentos()
                if self.next().word == ";":
                    self.declaracoes_variaveis()
                    self.declaracoes_subprogramas()
                    self.comando_composto()
                    return True
                else:
                    sys.exit("O ';' era esperado, mas não foi encontrador. Linha: " + str(self.current.line))
            else:
                sys.exit("Procedure sem identificador. Linha: " + str(self.current.line))
        else:
            self.index -= 1
            return False

    def argumentos(self):
        if self.next().word == "(":
            self.lista_de_parametros()
            if self.next().word == ")":
                pass
            else:
                sys.exit("Era esperado um ')'. Linha: " + str(self.current.line))
        else:
            self.index -= 1

    def lista_de_parametros(self):
        self.lista_de_identificadores()
        if self.next().word == ":":
            self.tipo()
            self.lista_de_parametros_ln()
        else:
            sys.exit("O ':' era esperado. Linha: " + str(self.current.line))

    def lista_de_parametros_ln(self):
        if self.next().word == ";":
            self.lista_de_identificadores()
            if self.next().word == ":":
                self.tipo()
                self.lista_de_parametros_ln()
            else:
                sys.exit("Era esparado ':'. Linha: " + str(self.current.line))
        else:
            self.index -= 1

    def comando_composto(self):
        if self.next().word == "begin":

            self.cont_begin_end += 1

            self.comandos_opcionais()
            if self.next().word == "end":

                self.cont_begin_end -= 1

                if not self.cont_begin_end:
                    self.tabela.pop_escopo()
                
                return True
            else:
                sys.exit("Comando 'end' não encontrado. Linha: " + str(self.current.line))
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
            tipo_var = self.tabela.get_simbolo_tipo(self.current.word)

            if self.next().word == ":=":
                self.expressao()

                if tipo_var == "integer" and self.pilha_tipos.topo() in ["real","boolean"]:
                    sys.exit("Incompatibilidade de tipos na atribuição para inteiro. Linha: " + str(self.current.line))

                elif tipo_var == "boolean" and self.pilha_tipos.topo() != "boolean":
                    sys.exit("Incompatibilidade de tipos na atribuição para booleana. Linha: " + str(self.current.line))

                elif tipo_var == "real" and self.pilha_tipos.topo() == "boolean":
                    sys.exit("Incompatibilidade de tipos na atribuição para real. Linha: " + str(self.current.line))

                else:
                    self.pilha_tipos.pop()
                return
            else:
                sys.exit("O ':=' era esperado")

        elif self.ativacao_de_procedimento():
            pass

        elif self.comando_composto():
            pass

        elif self.next().word == "if":
            self.expressao()

            if self.pilha_tipos.topo() != "boolean":
                sys.exit("Era esperado um valor booleano. Linha: " + str(self.current.line))
            else:
                self.pilha_tipos.pop()

            if self.next().word == "then":
                self.comando()
                self.parte_else()
                return
            else:
                sys.exit("O 'then' era eperado. Linha: " + str(self.current.line))
        else:
            self.index -= 1

        if self.next().word == "while":
            self.expressao()

            if self.pilha_tipos.topo() != "boolean":
                sys.exit("Era esperado um valor booleano. Linha: " + str(self.current.line))
            else:
                self.pilha_tipos.pop()

            if self.next().word == "do":
                self.comando()
            else:
                sys.exit("Era esperado um 'do'. Linha: " + str(self.current.line))
        else:
            self.index -= 1
        #>>>>>>>>>>>>>>>>>> Add Do-while <<<<<<<<<<<<<<<<<<
        if self.next().word == "do":
            self.comando()
            if self.next().word == ";":
                if self.next().word == "while":
                    if self.next().word == "(":
                        self.expressao()

                        if self.pilha_tipos.topo() != "boolean":
                            sys.exit("Era esperado um valor booleano. Linha: " + str(self.current.line))
                        else:
                            self.pilha_tipos.pop()

                        if self.next().word == ")":
                            pass
                        else:
                            sys.exit("Era esperado um ')' no final. Linha: " + str(self.current.line))
                    else:
                        sys.exit("Era esperado um '(' depois do 'while'. Linha: " + str(self.current.line))
                else:
                    sys.exit("Era esperado um 'while'. Linha: " + str(self.current.line))
            else:
                sys.exit("Falta finalizar com ';'. Linha: " + str(self.current.line))
        else:
            self.index -= 1
        #>>>>>>>>>>>>>>>>>> Add Do-while <<<<<<<<<<<<<<<<<<

    def parte_else(self):
        if self.next().word == "else":
            self.comando()
        else:
            self.index -= 1

    def variavel(self):
        if self.next().lex == "Identificador":
            
            self.verificar_id(self.current)

            return True
        else:
            self.index -= 1
            return False

    def ativacao_de_procedimento(self):
        if self.next().lex == "Identificador":

            self.verificar_id(self.current)

            if self.next().word == "(":
                self.lista_de_expressoes()
                if self.next().word == ")":
                    return True
                else:
                    sys.exit("O ')' era esperado. Linha: " + str(self.current.line))
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
            if not self.pilha_tipos.reduz_pct_relacional():
                sys.exit("Incompatibilidade de tipos. Linha: " + str(self.current.line))

    def expressao_simples(self):
        if self.termo():
            self.expressao_simples_ln()
        elif self.sinal():
            self.termo()
            self.expressao_simples_ln()
        else:
            sys.exit("Uma expressão era esperada. Linha: " + str(self.current.line))

    def expressao_simples_ln(self):
        if self.op_aditivo():
            op = self.current.word

            self.termo()
            self.expressao_simples_ln()

            if op == "or":
                if not self.pilha_tipos.reduz_pct_logico():
                    sys.exit("Incompatibilidade de tipos, eram esperados valores booleanos. Linha: " + str(self.current.line))
            else:
                if not self.pilha_tipos.reduz_pct():
                    sys.exit("Incompatibilidade de tipos. Linha: " + str(self.current.line))

    def termo(self):
        if self.fator():
            self.termo_ln()
            return True
        else:
            return False

    def termo_ln(self):
        if self.op_multiplicativo():
            op = self.current.word

            self.fator()
            self.termo_ln()

            if op == "and":
                if not self.pilha_tipos.reduz_pct_logico():
                    sys.exit("Incompatibilidade de tipos, eram esperado valores booleanos. Linha: " + str(self.current.line))
            else:
                if not self.pilha_tipos.reduz_pct():
                    sys.exit("Incompatibilidade de tipos. Linha: " + str(self.current.line))

    def fator(self):
        token = self.next()
        if token.lex == "Identificador":

            self.verificar_id(self.current)
            self.pilha_tipos.push(self.tabela.get_simbolo_tipo(self.current.word))

            if self.next().word == "(":
                self.lista_de_expressoes()
                if self.next().word == ")":
                    pass
                else:
                    sys.exit("Era esperado um ')'. Linha: " + str(self.current.line))
            else:
                self.index -= 1
                return True
        elif token.lex == "Número Inteiro":
            self.pilha_tipos.push("integer")

        elif token.lex == "Número Real":
            self.pilha_tipos.push("real")

        elif token.word in ["true","false"]:
            self.pilha_tipos.push("boolean")

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
