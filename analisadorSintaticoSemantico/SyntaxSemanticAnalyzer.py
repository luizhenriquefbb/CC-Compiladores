#!/usr/bin/python3
'''
Auth: Vinícius Matheus
Github: github.com/Vnicius
'''
import sys
import os

from analisadorSintaticoSemantico import SymbolsTable
from analisadorSintaticoSemantico import TypesStack

class SyntaxSemanticAnalyzer():
    def __init__(self, list_tokens):
        self.list_tokens = list_tokens  #lista de tokens
        self.current =  None    #token atual
        self.index = 0      #indíce do token atual
        self.tabela = SymbolsTable()    #tabela de símbolos
        self.cont_begin_end = 0     #contador de begin e end
        self.pilha_tipos = TypesStack()     #pilha de tipos

    def next(self):
        '''
        Retornar o próximo token da lista
        '''
        if self.index < len(self.list_tokens):  #verifica se o próximo índice pertence ao array
            self.current = self.list_tokens[self.index] #pega o token atual
            #print (self.current)
            self.index += 1
            return self.current

        sys.exit("Erro: O programa terminou, mas a análise não")    #caso chegue ao fim da lista sem terminar o programa
        return None

    def regride_token(self):
        self.index -= 1

    def push_id(self, token, type):
        '''
        Coloca um novo identificador na tabela de identificadores.
        '''
        self.tabela.push_simbolo(token.word, type)

    def has_id(self, token):
        '''
        Verifica se um identificador está na tabela de identificadores.
        '''
        if not self.tabela.simbolo_na_tabela(token.word):
            sys.exit("O símbolo '"+ token.word +"' na linha "+ str(token.line) +" não foi declarado")
    
    def verificar_id(self, token):
        '''
        Verifica se um idenficador está sendo usado ou declarado
        '''
        if self.cont_begin_end:
            self.has_id(token)
        else:
            self.push_id(token.word, ".")
    
    def verificar_procedimento(self, token):
        '''
        Verifica se o identificador é de um procedimento.
        '''
        if self.tabela.get_simbolo_tipo(token.word) == "procedure":
            return True

        return False
    
    def verfica_boolean(self):
        '''
        Verifica se o topo da pilha de tipos é booleano
        '''
        if self.pilha_tipos.topo() != "boolean":    #[SMT] verifica se o resultado da expressão é booleano
            sys.exit("Era esperado um valor booleano. Linha: " + str(self.current.line))
        else:
            self.pilha_tipos.pop()  #[SMT] se for boolean, esvazia a pilha

    def verficar_operacao(self, operador):
        '''
        Verifica se é uma operação lógica ou não e reduz a pilha de tipos
        '''
        if operador in ["and","or"]:
            if not self.pilha_tipos.reduz_pct_logico(): #[SMT] verifica se foi possível reduzir
                sys.exit("Incompatibilidade de tipos, eram esperado valores booleanos. Linha: " + str(self.current.line))
        else:
            if not self.pilha_tipos.reduz_pct():    #[SMT] verifica se foi possível reduzir
                sys.exit("Incompatibilidade de tipos. Linha: " + str(self.current.line))

    def startAnalysis(self):
        '''
        programa →
            program id;
            declarações_variáveis
            declarações_de_subprogramas
            comando_composto
            .
        '''
        if self.next().word == "program":   #verifica se começa com 'program'
            self.tabela.novo_escopo()   #[SMT] inicia um novo escopo na tabela

            if self.next().lex == "Identificador":  #verifica se o nome do programa foi declarado
                self.tabela.push_simbolo(self.current.word, "program")  #coloca o identifica do nome do programa na tabela

                if self.next().word == ";":     #fim do cabeçalho do programa
                    self.declaracoes_variaveis()    #procedimento de declaração de variáries
                    self.declaracoes_subprogramas() #procedimento de declaração de subprogramas
                    self.comando_composto()     #comandos do programa

                    if self.next().word == ".": #finalização do programa
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
        '''
        declarações_variáveis →
            var lista_declarações_variáveis
            | ε
        '''
        if self.next().word == "var":   #começo da declaração de variáveis
            self.lista_declaracoes_variaveis()  #procedimento para a lista de declarações de variáveis

        else:
            self.regride_token() 

    def lista_declaracoes_variaveis(self):
        '''
        lista_declarações_variáveis →
            lista_de_identificadores: tipo; lista_declarações_variáveis'
        '''
        if self.lista_de_identificadores(): #verifica a lista de identificadores

            if self.next().word == ":": #finalização da declaração de identificadores
                self.tipo()     #verifica se o tipo foi declarado

                if self.next().word == ";": #finalização da declaração da lista
                    self.lista_declaracoes_variaveis_ln()   #procedimento para a lista de declarações de variáveis

                else:
                    sys.exit("O ';' não enontrado. Linha: " + str(self.current.line))
            else:
                sys.exit("O ':' não foi encontrado. Linha: " + str(self.current.line))
        else:
            sys.exit("Era esperado um identificador. Linha: " + str(self.current.line))

    def lista_declaracoes_variaveis_ln(self):
        '''
        lista_declarações_variáveis’ →
            lista_de_identificadores: tipo; lista_declarações_variáveis' 
            | ε
        '''
        if self.lista_de_identificadores(): #verifica se é uma lista de identificadores

            if self.next().word == ":": #finalização da declaração de identificadores
                self.tipo()

                if self.next().word == ";":
                    self.lista_declaracoes_variaveis_ln()   #procedimento para a lista de declarações de variáveis

                else:
                    sys.exit("O ';' não enontrado. Linha: " + str(self.current.line))
            else:
                sys.exit("O ':' não foi encontrado. Linha: " + str(self.current.line))

    def lista_de_identificadores(self):
        '''
        lista_de_identificadores →
            id lista_de_identificadores’
        '''
        if self.next().lex == "Identificador":  #verifica se é um identificador

            self.push_id(self.current, ".")     #[SMT] coloca o identificador na tabela sem tipo
            
            self.lista_de_identificadores_ln()  #procedimento para a lista de identificadores
            return True

        else:
            self.regride_token()
            return False

    def lista_de_identificadores_ln(self):
        '''
        lista_de_identificadores’ →
            , id lista_de_identificadores’ 
            | ε 
        '''
        if self.next().word == ",":
            if self.next().lex == "Identificador":  #verifica se é um identificador

                self.push_id(self.current, ".") #[SMT] coloca o identificador na tabela sem tipo

                self.lista_de_identificadores_ln()

            else:
                sys.exit("Era esperado um identificador. Linha: " + str(self.current.line))
        else:
            self.regride_token()

    def tipo(self):
        '''
        tipo →
            integer
            | real
            | boolean
        '''
        if self.next().word in ["integer","real","boolean"]:    #verifica se é um tipo válido

            self.tabela.set_tipo(self.current.word) #[SMT] acrescenta o tipo nos identificadores sem tipo

        else:
            sys.exit("Não é um tipo")

    def declaracoes_subprogramas(self):
        '''
        declarações_de_subprogramas →
            declarações_de_subprogramas’ε
        '''
        self.declaracoes_subprogramas_ln()  #procedimeno para a declaração de subprogramas

    def declaracoes_subprogramas_ln(self):
        '''
        declarações_de_subprogramas’ →
            declaração_de_subprograma; declarações_de_subprogramas’ 
            |  ε
        '''
        if self.declaracao_subprograma():   #verifica se é uma declaração de subprograma

            if self.next().word == ";":     #verifica o fim da declaração
                self.declaracoes_subprogramas_ln()  #procedimento para a lista de declarações de subprograma

            else:
                sys.exit("Declaração de subprograma sem ';'. Linha: " + str(self.current.line))

    def declaracao_subprograma(self):
        '''
        declaração_de_subprograma →
            procedure id argumentos;
            declarações_variáveis
            declarações_de_subprogramas
            comando_composto
        '''
        if self.next().word == "procedure":     #verifica se começa com 'procedure'
            if self.next().lex == "Identificador":  #verifica o nome do subprograma

                self.tabela.push_simbolo(self.current.word,"procedure") #[SMT] acrescente o identificador do nome na tabela com o tipo 'procedure'
                self.tabela.novo_escopo()   #[SMT] inicia um novo escopo na tabela

                self.argumentos()   #verifica a lista de argumentos do subprograma

                if self.next().word == ";":
                    self.declaracoes_variaveis()    #verifica a delcaração de variáveis
                    self.declaracoes_subprogramas() #verifica novas declarações de subprogramas
                    self.comando_composto()     #verifica os comandos do subprograma
                    return True

                else:
                    sys.exit("O ';' era esperado, mas não foi encontrador. Linha: " + str(self.current.line))
            else:
                sys.exit("Procedure sem identificador. Linha: " + str(self.current.line))
        else:
            self.regride_token()
            return False

    def argumentos(self):
        '''
        argumentos →
            (lista_de_parametros)
            | ε
        '''
        if self.next().word == "(":
            self.lista_de_parametros()  #procedimento para a lista de argumentos
            
            if self.next().word != ")": #verifica o fim da declaração de argumentos
                sys.exit("Era esperado um ')'. Linha: " + str(self.current.line))
        else:
            self.regride_token()

    def lista_de_parametros(self):
        '''
        lista_de_parametros →
            lista_de_identificadores: tipo lista_de_parametros’
        '''
        self.lista_de_identificadores() #verifica a lista de identificadores

        if self.next().word == ":": #verifica o fim da lista de identificadores
            self.tipo()
            self.lista_de_parametros_ln()

        else:
            sys.exit("O ':' era esperado. Linha: " + str(self.current.line))

    def lista_de_parametros_ln(self):
        '''
        lista_de_parametros’ →
            ; lista_de_identificadores: tipo lista_de_parametros’ 
            | ε
        '''
        if self.next().word == ";":
            self.lista_de_identificadores() #verifica a lista de identificadores

            if self.next().word == ":": #verfica o fim da lista de identificadores
                self.tipo()
                self.lista_de_parametros_ln()

            else:
                sys.exit("Era esparado ':'. Linha: " + str(self.current.line))
        else:
            self.regride_token()

    def comando_composto(self):
        '''
        comando_composto →
            begin
            comandos_opcionais
            end
        '''
        if self.next().word == "begin": #verifica se começa com 'begin'
            self.cont_begin_end += 1    #[SMT] incrementa o contador de begin-end
            self.comandos_opcionais()   #verifica o uso de comando opcionais

            if self.next().word == "end":
                self.cont_begin_end -= 1    #[SMT] decrementa o contador de begin-end

                if not self.cont_begin_end: #[SMT] confere se o contador de begin-end é 0
                    self.tabela.pop_escopo()    #[SMT] remove o escopo atual da tabela
                
                return True
            else:
                sys.exit("Comando 'end' não encontrado. Linha: " + str(self.current.line))
        else:
            
            self.regride_token()
            return False

    def comandos_opcionais(self):
        '''
            comandos_opcionais →
            lista_de_comandos
            | ε
        '''
        self.lista_de_comandos()    #procedimento para a lista de comandos

    def lista_de_comandos(self):
        '''
        lista_de_comandos →
            comando lista_de_comandos’
        '''
        self.comando()  #verifica os comandos
        self.lista_de_comandos_ln() #procedimento para a lista de comandos


    def lista_de_comandos_ln(self):
        '''
        lista_de_comandos’ →
            ; comando lista_de_comandos’ 
            | ε
        '''
        if self.next().word == ";": #verifica o fim do comando anterior
            self.comando()  #verifica so comandos
            self.lista_de_comandos_ln() #procedimento para a lista de comandos

        else:
            self.regride_token()

    def comando(self):
        '''
        comando →
            variável := expressão
            | ativação_de_procedimento
            | comando_composto
            | if expressão then comando parte_else
            | while expressão do comando
            | do comando while (expressão)
        '''
        if self.variavel(): #verifica se é um variável
            tipo_var = self.tabela.get_simbolo_tipo(self.current.word)  #[SMT] guarda o tipo da variável

            if self.next().word == ":=":    #verifica o símbolo de atribuição
                self.expressao()    #verifica a expressão

                #[SMT] confere se o tipo resultante da expressão é equivalente ao tipo da variável
                if tipo_var == "integer" and self.pilha_tipos.topo() in ["real","boolean"]:
                    sys.exit("Incompatibilidade de tipos na atribuição para inteiro. Linha: " + str(self.current.line))

                elif tipo_var == "boolean" and self.pilha_tipos.topo() != "boolean":
                    sys.exit("Incompatibilidade de tipos na atribuição para booleana. Linha: " + str(self.current.line))

                elif tipo_var == "real" and self.pilha_tipos.topo() == "boolean":
                    sys.exit("Incompatibilidade de tipos na atribuição para real. Linha: " + str(self.current.line))

                else:
                    self.pilha_tipos.pop()  #[SMT] se for compatível, então esvaiza a pilha
                return
            else:
                sys.exit("O ':=' era esperado")

        elif self.ativacao_de_procedimento():   #verifica se é uma ativação de procedimento
            pass

        elif self.comando_composto():   #verifica se é um comando composto
            pass

        elif self.next().word == "if":  #verifica se é o comando 'if'
            self.expressao()    #verifica a expressão

            self.verfica_boolean() #verifica se o resultado da expressão é booleano

            if self.next().word == "then":  #verifica se o 'then' foi usado
                self.comando()  #verifica os comandos
                self.parte_else()   #verifica a ocorrência do 'else'
                return
            else:
                sys.exit("O 'then' era eperado. Linha: " + str(self.current.line))
        else:
            self.regride_token()

        if self.next().word == "while": #verifica se é o comando 'while'
            self.expressao()    #verifica a expressão

            self.verfica_boolean() #verifica se o resultado da expressão é booleano

            if self.next().word == "do":    #verifica a ocorrência do 'do'
                self.comando()  #verifica o comando
            else:
                sys.exit("Era esperado um 'do'. Linha: " + str(self.current.line))
        else:
            self.regride_token()

        #>>>>>>>>>>>>>>>>>> Modificação: Do-while <<<<<<<<<<<<<<<<<<
        if self.next().word == "do":    #verifica se é o comando do-while
            self.comando()  #verifica os comandos

            if self.next().word == ";":

                if self.next().word == "while": #verifica a ocorrência do 'while'
                    
                    if self.next().word == "(":
                        self.expressao()    #verifica a expressão

                        self.verfica_boolean() #verifica se o resultado da expressão é booleano

                        if self.next().word != ")": #verifica o fim do 'do-while'
                            sys.exit("Era esperado um ')' no final. Linha: " + str(self.current.line))
                    else:
                        sys.exit("Era esperado um '(' depois do 'while'. Linha: " + str(self.current.line))
                else:
                    sys.exit("Era esperado um 'while'. Linha: " + str(self.current.line))
            else:
                sys.exit("Falta finalizar com ';'. Linha: " + str(self.current.line))
        else:
            self.regride_token()
        #>>>>>>>>>>>>>>>>>> Modificação: Do-while <<<<<<<<<<<<<<<<<<

    def parte_else(self):
        '''
        parte_else →
            else comando
            | ε
        '''
        if self.next().word == "else":  #verifica a ocorrência do 'else'
            self.comando()  #verifica os comandos

        else:
            self.regride_token() 

    def variavel(self):
        '''
        variável →
            id
        '''
        if self.next().lex == "Identificador":  #verifica se é um identificador
            
            #[SMT] verifica se é um identificador de procedimento
            if self.verificar_procedimento(self.current):
                self.regride_token() 
                return False

            self.verificar_id(self.current) #[SMT] verifica se o identificador está na tabela

            return True
        else:
            self.regride_token() 
            return False

    def ativacao_de_procedimento(self):
        '''
        ativação_de_procedimento →
            id
            | id (lista_de_expressões)
        '''
        if self.next().lex == "Identificador":  #verifica se é um identificador
            self.has_id(self.current)   #[SMT] verifica se o identificador está na tabela

            if self.next().word == "(":
                self.lista_de_expressoes()  #verifica a lista de expressões

                if self.next().word == ")": #fim da ativação de procedimento
                    return True
                else:
                    sys.exit("O ')' era esperado. Linha: " + str(self.current.line))
            else:
                self.regride_token() 
                return True
        else:
            self.regride_token() 
            return False

    def lista_de_expressoes(self):
        '''
        lista_de_expressões →
            expressão lista_de_expressões’
        '''
        self.expressao()    #verifica a expressão inicial
        self.lista_de_expressoes_ln()   #procedimento da lista de expressões

    def lista_de_expressoes_ln(self):
        '''
        lista_de_expressões’ →
            , expressão lista_de_expressões’
            | ε
        '''
        if self.next().word == ",":
            self.expressao()    #verifica a expressão
            self.lista_de_expressoes_ln()   #procedimento da lista de expressões

        else:
            self.regride_token() 

    def expressao(self):
        '''
        expressão →
            expressão_simples
            | expressão_simples op_relacional expressão_simples
        '''
        self.expressao_simples()    #verifica uma expressão simples

        if self.op_relacional():    #verifica o operador relacional
            self.expressao_simples()

            #[SMT] verifica a pilha de tipos
            if not self.pilha_tipos.reduz_pct_relacional():
                sys.exit("Incompatibilidade de tipos. Linha: " + str(self.current.line))

    def expressao_simples(self):
        '''
        expressão_simples →
            termo expressão_simples’
            | sinal termo  expressão_simples’
        '''
        if self.termo():    #verifica o termos da expressão
            self.expressao_simples_ln() #procedimento para a expressão simples

        elif self.sinal():  #verifica o sinal   
            self.termo()
            self.expressao_simples_ln()

        else:
            sys.exit("Uma expressão era esperada. Linha: " + str(self.current.line))

    def expressao_simples_ln(self):
        '''
        expressão_simples’ →
            op_aditivo termo expressão_simples’
            | ε
        '''
        if self.op_aditivo():   #verifica o operador aditivo
            op = self.current.word  #[SMT] guarda o operador usado

            self.termo()
            self.expressao_simples_ln()

            self.verficar_operacao(op) #[SMT] verifica se a operação é válida

    def termo(self):
        '''
        termo →
            fator termo’
        '''
        if self.fator():    #verifica o fator
            self.termo_ln() #procediemnto para verificar o termo
            return True

        else:
            return False

    def termo_ln(self):
        '''
        termo’ →
            op_multiplicativo fator termo’
            | ε
        '''
        if self.op_multiplicativo():    #verifica o operador multiplicativo
            op = self.current.word  #[SMT] guarda o operador usado

            self.fator()
            self.termo_ln()

            self.verficar_operacao(op) #verifica se a operação é válida

    def fator(self):
        '''
        fator →
            id
            | id(lista_de_expressões)
            | num_int
            | num_real
            | true
            | false
            | (expressão)
            | not fator
        '''
        token = self.next()

        if token.lex == "Identificador":    #verifica se é um identificador

            self.has_id(self.current)   #[SMT] verifica se o identificador está na tabela
            
            #[SMT] coloca o tipo do identificador na pilha de tipos
            self.pilha_tipos.push(self.tabela.get_simbolo_tipo(self.current.word))

            if self.next().word == "(":
                self.lista_de_expressoes()  #procedimento para a lista de expressões

                if self.next().word != ")":
                    sys.exit("Era esperado um ')'. Linha: " + str(self.current.line))
            else:
                self.regride_token()
                return True

        elif token.lex == "Número Inteiro":     #verifica se é um número inteiro
            self.pilha_tipos.push("integer")

        elif token.lex == "Número Real":    #verifica se é um número real
            self.pilha_tipos.push("real")

        elif token.word in ["true","false"]:    ##verifica se é um vaor booleano
            self.pilha_tipos.push("boolean")

        elif token.word == "(":
            self.expressao()    #procedimento para verifica a expressão

            if self.next().word != ")":
                sys.exit("Falta o ')'")

        elif token.word == "not":
            self.fator()    #procedimento para verificar o fator

        else:
            self.regride_token()
            return False

        return True

    def sinal(self):
        '''
        sinal →
            + | -
        '''
        if self.next().word in "+-":    #verifica se o sinal é '+' ou '-'
            return True

        else:
            self.regride_token()
            return False

    def op_relacional(self):
        '''
        op_relacional →
            = | < | > | <= | >= | <>
        '''
        #verifica se está na lista de operadores relacionais
        if self.next().word in ["=","<",">","<=",">=","<>"]:
            return True

        else:
            self.regride_token()
            return False

    def op_aditivo(self):
        '''
        op_aditivo →
            + | - | or
        '''
        #verifica se está na lista de operadores aditivos
        if self.next().word in ["+","-","or"]:
            return True

        else:
            self.regride_token()
            return False

    def op_multiplicativo(self):
        '''
        op_multiplicativo →
            * | / | and
        '''
        #verifica se está na lista de operadores multiplicativos
        if self.next().word in ["*","/","and"]:
            return True

        else:
            self.regride_token()
            return False

############################

if __name__ == "__main__":
     with open(sys.argv[1],"r") as program:
        lex = LexicalAnalyzer.LexicalAnalyzer()
        syn = SyntaxAnalyzer(lex.analyze(program.read()))
        if (syn.startAnalysis()):
            print("PROGRAMA OK!")
