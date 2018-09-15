 # -*- coding: utf-8 -*- 

from util import *
import sys

from symbolsTable import SymbolsTable
from typesStack import TypesStack

# Default object for a token
current_token = {
    'token': '',
    'classification': '',
    'line': ''
}

# global auxiliary objects
tabela = SymbolsTable()
pilha_tipos = TypesStack()

cont_begin_end = 0 # counter of begin and ends



def sintatico (_input):
    global current_token, tokens, tabela, pilha_tipos

    tokens = _input

    # get and remove first token
    current_token = tokens.pop(0)

    # if fails stop analisys
    if not PROGRAMA():
        return False

    # only true if read all tokens
    if len(tokens) != 0:
        return False


    return True

def print_error(expected, line=None):
    global current_token, tabela, pilha_tipos
    
    if line == None:
        line = current_token['line']

    # print ("erro: expected: '"+ expected +"' at line " + str(line)+". Found '"+current_token['token']+"'", end='\r') #python 3
    sys.stdout.write('\r'+"erro: expected: '"+ expected +"' at line " + str(line)+". Found '"+current_token['token']+"'")
    sys.stdout.write("\033[K")
    sys.stdout.flush() #python 2

def getSimbol():
    global current_token, tabela, pilha_tipos
    current_token = tokens.pop(0)
    # return current_token

def regride_token():
    global current_token

    tokens.insert(0, current_token)



# =======================================

def push_id(token, type):
    '''
    Coloca um novo identificador na tabela de identificadores.
    '''
    global tabela

    tabela.push_simbolo(token, type)

def has_id(token):
    '''
    Verifica se um identificador está na tabela de identificadores.
    '''
    global tabela
    if not tabela.simbolo_na_tabela(token['token']):
        sys.exit("O símbolo '"+ token['token'] +"' na linha "+ str(token['line']) +" não foi declarado")

def verificar_id(token):
    '''
    Verifica se um idenficador está sendo usado ou declarado
    '''
    global cont_begin_end

    if cont_begin_end:
        has_id(token)
    else:
        push_id(token['token'], ".")

def verificar_procedimento(token):
    '''
    Verifica se o identificador é de um procedimento.
    '''
    global tabela

    if tabela.get_simbolo_tipo(token['token']) == "procedure":
        return True

    return False

def verfica_boolean():
    '''
    Verifica se o topo da pilha de tipos é booleano
    '''
    global pilha_tipos, current_token

    if pilha_tipos.topo() == "boolean":    #[SMT] verifica se o resultado da expressão é booleano
        pilha_tipos.pop()  #[SMT] se for boolean, esvazia a pilha
    else:
        sys.exit("Era esperado um valor booleano. Linha: " + str(current_token['line']))

def verficar_operacao(operador):
    '''
    Verifica se é uma operação lógica ou não e reduz a pilha de tipos
    '''
    global pilha_tipos, current_token
    
    if operador in ["and","or"]:
        if not pilha_tipos.reduz_pct_logico(): #[SMT] verifica se foi possível reduzir
            sys.exit("Incompatibilidade de tipos, eram esperado valores booleanos. Linha: " + str(current_token['line']))
    else:
        if not pilha_tipos.reduz_pct():    #[SMT] verifica se foi possível reduzir
            sys.exit("Incompatibilidade de tipos. Linha: " + str(current_token['line']))



# ==========================================



def PROGRAMA():
    """
    PROGRAMA 
        program id;
        DECLARACOES_VARIAVEIS
        DECLARACOES_DE_SUBPROGRAMAS
        COMANDO_COMPOSTO
        .
    """
    global current_token, tabela, pilha_tipos

    if current_token['token'] == 'program':
        tabela.novo_escopo()
        getSimbol()
        if current_token['classification'] == 'Id\t\t':
            tabela.push_simbolo(current_token['token'], 'program') #coloca o identificador do nome do programa na tabela
            
            getSimbol()
            
            
            if current_token['token'] == ';':
                getSimbol()
                if not DECLARACOES_VARIAVEIS():
                    return False
                
                if not DECLARACOES_DE_SUBPROGRAMAS():
                    return False
                
                if not COMANDO_COMPOSTO():
                    return False
                
                if current_token['token'] == '.':
                    sys.stdout.write('\r'+"")
                    sys.stdout.write("\033[K")
                    sys.stdout.flush() #python 2
                    return True

                else:
                    print_error('.')
                    return False
                
                
            else:
                print_error(';')
                return False
        else:
            print_error('id')
            return False
    else:
        print_error('program')
        return False

    sys.stdout.write('\r'+"")
    sys.stdout.write("\033[K")
    sys.stdout.flush() #python 2
    return True

def DECLARACOES_VARIAVEIS():
    """
    DECLARACOES_VARIAVEIS 
        var LISTA_DECLARACOES_VARIAVEIS
        | e
    """
    global current_token, tabela, pilha_tipos

    if current_token['token'] == 'var':
        getSimbol()
        if not LISTA_DECLARACOES_VARIAVEIS():
            return False
    else:
        return True # vazio

    return True

def LISTA_DECLARACOES_VARIAVEIS():
    """
    LISTA_DECLARACOES_VARIAVEIS 
        LISTA_DE_IDENTIFICADORES: TIPO; LISTA_DECLARACOES_VARIAVEIS_2
    """
    global current_token, tabela, pilha_tipos
    
    if not LISTA_DE_IDENTIFICADORES():
        return False
    
    if current_token['token'] == ':':
        getSimbol()
        if not TIPO():
            return False

        if current_token['token'] == ';':
            getSimbol()
            if not LISTA_DECLARACOES_VARIAVEIS_2():
                return False
        
        else:
            print_error(';')
            return False

    else:
        print_error(':')
        return False
    
    # getSimbol()
    return True

def LISTA_DECLARACOES_VARIAVEIS_2():
    """
    LISTA_DECLARACOES_VARIAVEIS_2 : {
        LISTA_DE_IDENTIFICADORES: TIPO; LISTA_DECLARACOES_VARIAVEIS_2
        | e

    }
    """
    global current_token, tabela, pilha_tipos

    if not LISTA_DE_IDENTIFICADORES():
        return True # vazio
    
    if current_token['token'] == ':':
        getSimbol()
        if not TIPO():
            return False

        if current_token['token'] == ';':
            getSimbol()
            if not LISTA_DECLARACOES_VARIAVEIS_2():
                return False
        
        else:
            print_error(';')
            return False

    else:
        print_error(':')
        return False

    # getSimbol()
    return True

def LISTA_DE_IDENTIFICADORES():
    """
    LISTA_DE_IDENTIFICADORES 
        id LISTA_DE_IDENTIFICADORES_2
    """
    global current_token, tabela, pilha_tipos

    if current_token['classification'] == 'Id\t\t':
        push_id(current_token['token'], ".")     #[SMT] coloca o identificador na tabela sem tipo

        getSimbol()


        if not LISTA_DE_IDENTIFICADORES_2():
            return False


    else:
        print_error('id')
        return False

    # getSimbol()
    return True

def LISTA_DE_IDENTIFICADORES_2():
    """
    LISTA_DE_IDENTIFICADORES_2 
        , id LISTA_DE_IDENTIFICADORES_2
        | e
    """
    global current_token, tabela, pilha_tipos
    if current_token['token'] == ',':
        getSimbol()
        if current_token['classification'] == 'Id\t\t':
            push_id(current_token['token'], ".") #[SMT] coloca o identificador na tabela sem tipo

            getSimbol()


            if not LISTA_DE_IDENTIFICADORES_2():
                return False
        else:
            print_error('id')
            return False
    else:
        return True # vazio

    # getSimbol()
    return True

def TIPO():
    """
    TIPO 
        integer
        | real
        | boolean
    """
    global current_token, tabela, pilha_tipos

    if current_token['token'] == 'integer' or current_token['token'] == 'real' or current_token['token'] == 'boolean':
        tabela.set_tipo(current_token['token']) #[SMT] acrescenta o tipo nos identificadores sem tipo

        getSimbol()


        return True

    else:
        print_error("'inteiro/real/boo;lean")
        return False

def DECLARACOES_DE_SUBPROGRAMAS():
    """
    DECLARACOES_DE_SUBPROGRAMAS 
        | DECLARACOES_DE_SUBPROGRAMAS_2
    """

    global current_token, tabela, pilha_tipos

    if not DECLARACOES_DE_SUBPROGRAMAS_2():
        return False

    else:
        # getSimbol()
        return True

def DECLARACOES_DE_SUBPROGRAMAS_2():
    """
    DECLARACOES_DE_SUBPROGRAMAS_2 
        DECLARACAO_DE_SUBPROGRAMA; DECLARACOES_DE_SUBPROGRAMAS_2
        | e
    """

    global current_token, tabela, pilha_tipos

    if not DECLARACAO_DE_SUBPROGRAMA():
        return True # vazio

    else:
        if current_token['token'] == ';':
            getSimbol()
            
            if not DECLARACOES_DE_SUBPROGRAMAS_2():
                return False

            
        else:
            print_error(';')
            return False

    # getSimbol()
    return True

def DECLARACAO_DE_SUBPROGRAMA():
    """
    DECLARACAO_DE_SUBPROGRAMA 
        procedure id ARGUMENTOS;
        DECLARACOES_VARIAVEIS
        DECLARACOES_DE_SUBPROGRAMAS
        COMANDO_COMPOSTO
    """

    global current_token, tabela, pilha_tipos
    
    if current_token['token'] == 'procedure':
        getSimbol()
        if current_token['classification'] == 'Id\t\t':

            tabela.push_simbolo(current_token['token'],"procedure") #[SMT] acrescenta o identificador do nome na tabela com o tipo 'procedure'
            tabela.novo_escopo()   #[SMT] inicia um novo escopo na tabela

            getSimbol()

            if not ARGUMENTOS():
                return False

            if current_token['token'] == ';':
                getSimbol()

                if not DECLARACOES_VARIAVEIS():
                    return False

                if not DECLARACOES_DE_SUBPROGRAMAS():
                    return False

                if not COMANDO_COMPOSTO():
                    return False

            else:
                print_error(';')
                return False

        else:
            print_error('id')
            return False
    else:
        print_error('procedure')
        return False


    # getSimbol()
    return True

def ARGUMENTOS():
    """
    ARGUMENTOS 
        (LISTA_DE_PARAMETROS)
        | e
    """
    if current_token['token'] == '(':
        getSimbol()
        if not LISTA_DE_PARAMETROS():
            return False

        if current_token['token'] == ')':
            getSimbol()
            return True

        else:
            print_error(')')
            return False

    else:
        return True # vazio
    
    
    # getSimbol()
    return True

def LISTA_DE_PARAMETROS():
    """
    LISTA_DE_PARAMETROS
        LISTA_DE_IDENTIFICADORES: TIPO LISTA_DE_PARAMETROS_2
    """
    global current_token, tabela, pilha_tipos

    if LISTA_DE_IDENTIFICADORES() == False:
        return False
        
        
    if current_token['token'] == ":":
        getSimbol()

        if TIPO() == False:
            return False

        if LISTA_DE_PARAMETROS_2() == False:
            return False

    # getSimbol()
    return True

def LISTA_DE_PARAMETROS_2():
    """
    LISTA_DE_PARAMETROS_2:
        ; LISTA_DE_IDENTIFICADORES: TIPO LISTA_DE_PARAMETROS_2
        | e	
    """
    global current_token, tabela, pilha_tipos

    if current_token['token'] == ';':
        getSimbol()

        if LISTA_DE_IDENTIFICADORES() == False:
            return False

        if current_token['token'] == ':':
            getSimbol()

            if TIPO() == False:
                return False

            if LISTA_DE_PARAMETROS_2() == False:
                return False

        else:
            print_error(':')
            return False

    else:
        return True # vazio


    return True

# Ponto e virgula
def COMANDO_COMPOSTO():
    """
    COMANDO_COMPOSTO
        begin
        COMANDOS_OPCIONAIS
        COMANDO_COMPOSTO_DESAMBIGUIDADE
    """
    global current_token, tabela, pilha_tipos, cont_begin_end

    if current_token['token'] == 'begin':
        cont_begin_end += 1    #[SMT] incrementa o contador de begin-end
        
        getSimbol()
        
        if COMANDOS_OPCIONAIS() == False:
            return False

        if not COMANDO_COMPOSTO_DESAMBIGUIDADE():
           return False
        

    else:
        print_error('begin')
        return False


    # getSimbol()
    return True

def COMANDO_COMPOSTO_DESAMBIGUIDADE():
    """
    COMANDO_COMPOSTO_DESAMBIGUIDADE
        ; end
        | end
    """

    global cont_begin_end, tabela


    if current_token['token'] == ";":
        getSimbol()
        if current_token['token'] == 'end':
            getSimbol()
            
            cont_begin_end -= 1    #[SMT] decrementa o contador de begin-end
            if not cont_begin_end: #[SMT] confere se o contador de begin-end é 0
                tabela.pop_escopo()    #[SMT] remove o escopo atual da tabela

        else:
            print_error("end")
            return False
    else:
        if current_token['token'] == 'end':
            getSimbol()
            
            cont_begin_end -= 1    #[SMT] decrementa o contador de begin-end
            if not cont_begin_end: #[SMT] confere se o contador de begin-end é 0
                tabela.pop_escopo()    #[SMT] remove o escopo atual da tabela

        else:
            print_error("';' or 'end'")
            return False

    return True

def COMANDOS_OPCIONAIS():
    """
    COMANDOS_OPCIONAIS
        LISTA_DE_COMANDOS
        | e
    """

    global current_token, tabela, pilha_tipos

    if LISTA_DE_COMANDOS() == False:
        return False
    else:
        return True #vazio

    # getSimbol()
    return True

def LISTA_DE_COMANDOS():
    """
    LISTA_DE_COMANDOS
        COMANDO LISTA_DE_COMANDOS_2
    """
    global current_token, tabela, pilha_tipos

    if COMANDO() == False:
        return False

    if LISTA_DE_COMANDOS_2() == False:
        return False


    # getSimbol()
    return True

def LISTA_DE_COMANDOS_2():
    """
    LISTA_DE_COMANDOS_2 : {
        ; COMANDO LISTA_DE_COMANDOS_2
        | e
    }
    """

    if current_token['token'] == ';':
        getSimbol()
        if COMANDO() == False:
            # return False
        # gambiarra ================
            return True # ';' opcional
        # ============================
        

        if LISTA_DE_COMANDOS_2() == False:
            return False

    else:
        return True #vazio

    return True

def COMANDO():
    """
    COMANDO :
        VARIAVEL := EXPRESSAO
        | ATIVACAO_DE_PROCEDIMENTO
        | COMANDO_COMPOSTO
        | if EXPRESSAO then COMANDO PARTE_ELSE
        | while EXPRESSAO do COMANDO
        # modificacao: do LISTA_DE_COMANDOS while (EXPRESSAO)
    """
    global tabela, current_token, pilha_tipos
    
    tipo_var = tabela.get_simbolo_tipo(current_token['token'])  #[SMT] guarda o tipo da variável

    if not VARIAVEL():
        if not ATIVACAO_DE_PROCEDIMENTO():
            if not COMANDO_COMPOSTO():
                if current_token['token'] == 'if':
                    getSimbol()
                    if not EXPRESSAO():
                        return False

                    if current_token['token'] == 'then':
                        getSimbol()
                        if not COMANDO():
                            return False

                        if not PARTE_ELSE():
                            return False

                    else:
                        print_error("then")
                        return False


                elif current_token['token'] == 'while':
                    getSimbol()

                    if not EXPRESSAO():
                        return False

                    if current_token['token'] == 'do':
                        getSimbol()
                        if not COMANDO(): return False
                    else:
                        print_error("do")
                        return False

                # =============== MODIFICACAO AULA ==================
                elif current_token['token'] == 'do':
                    getSimbol()
                    if LISTA_DE_COMANDOS() == False:
                        return False
                    
                    if current_token['token'] == 'while':
                        getSimbol()

                        if current_token['token'] == '(':
                            getSimbol()

                            if EXPRESSAO() == False:
                                return False

                            if current_token['token'] == ')':
                                getSimbol()
                                return True

                            
                        else:
                            print_error('(')
                            return False

                    else:
                        print_error('while')
                        return False


                else:

                    print_error("'if' or 'while' or 'do")
                    return False

                # ===============================================

    else:



        if current_token['token'] == ':=':
            getSimbol()

            if not EXPRESSAO():
                return False
        
            #[SMT] confere se o tipo resultante da expressão é equivalente ao tipo da variável
            if tipo_var == "integer" and pilha_tipos.topo() in ["real","boolean"]:
                sys.exit("Incompatibilidade de tipos na atribuição para inteiro. Linha: " + str(current_token['line']))

            elif tipo_var == "boolean" and pilha_tipos.topo() != "boolean":
                sys.exit("Incompatibilidade de tipos na atribuição para booleana. Linha: " + str(current_token['line']))

            elif tipo_var == "real" and pilha_tipos.topo() == "boolean":
                sys.exit("Incompatibilidade de tipos na atribuição para real. Linha: " + str(current_token['line']))

            else:
                pilha_tipos.pop()  #[SMT] se for compatível, então esvaiza a pilha

        else:
            print_error(':=')
            return False



    return True

def PARTE_ELSE():
    """
    PARTE_ELSE :
        else COMANDO
        | e
    """

    global current_token, tabela, pilha_tipos

    if current_token['token'] == 'else':
        getSimbol()

        if not COMANDO(): return False

    else:
        return True # vazio

    return True

def VARIAVEL():
    """
    VARIAVEL :
	    id
    """
    global current_token, tabela, pilha_tipos
    if current_token['classification'] == 'Id\t\t':
        # TODO: [SMT] verifica se é um identificador de procedimento
        if verificar_procedimento(current_token):
            # regride_token()
            return False

        verificar_id(current_token) #[SMT] verifica se o identificador está na tabela
        
        getSimbol()
        return True 

    else:
        print_error('Id')
        return False

def ATIVACAO_DE_PROCEDIMENTO():
    """
    ATIVACAO_DE_PROCEDIMENTO :
	    id ATIVACAO_DE_PROCEDIMENTO_DESAMBIGUIDADE
    """

    global current_token, tabela, pilha_tipos

    if current_token['classification'] == 'Id\t\t':
        has_id(current_token)   #[SMT] verifica se o identificador está na tabela

        getSimbol()

        if not ATIVACAO_DE_PROCEDIMENTO_DESAMBIGUIDADE(): return False

    else:
        print_error('id')
        return False

    return True

def ATIVACAO_DE_PROCEDIMENTO_DESAMBIGUIDADE():
    """
    ATIVACAO_DE_PROCEDIMENTO_DESAMBIGUIDADE :
        (LISTA_DE_EXPRESSOES)
        | e
    """
    global current_token, tabela, pilha_tipos
    
    if current_token['token'] == '(':
        getSimbol()
        if not LISTA_DE_EXPRESSOES(): return False
        
        if current_token['token'] == ')':
            getSimbol()
            return True

        else:
            print_error(')')
            return False

    else:
        return True # vazio
    
    return True

def OP_MULTIPLICATIVO():
    """
    OP_MULTIPLICATIVO :
        *
        | /
        | and
    """

    global current_token, tabela, pilha_tipos

    if current_token['token'] == '*' or current_token['token'] == '/' or current_token == 'and':
        getSimbol()
        return True
    else:
        print_error("'*', '/' or 'and'")
        return False

def OP_ADITIVO():
    """
    OP_ADITIVO :
        +
        | -
        | or
    """

    global current_token, tabela, pilha_tipos
    if current_token['token'] == '+' or current_token['token'] == '-' or current_token['token'] == 'or':
        getSimbol()
        return True
    else:
        print_error("'+', '-', or 'or'")
        return False

def OP_RELACIONAL():
    """
    OP_RELACIONAL :
        =
        | <
        | >
        | <=
        | >=
        | <>
    """

    global current_token, tabela, pilha_tipos
    if current_token['token'] == '=' or current_token['token'] == '<' or current_token['token'] == '>' or current_token['token'] == '<=' or current_token['token'] == '>=' or current_token['token'] == '<>':
        getSimbol()
        return True
    else:
        print_error("'=', '<', '>', '<=', '>=' or '<>'")
        return False

def SINAL():
    """
    SINAL :
        + 
        | -
    """

    global current_token, tabela, pilha_tipos
    if current_token['token'] == '+' or current_token['token'] == '-':
        getSimbol()
        return True
    else:
        print_error("'+' or '-'")
        return False

def FATOR():
    """
    FATOR :
        id FATOR_DESAMBIGUIDADE
        | NUM_INT
        | NUM_REAL
        | true
        | false
        | (EXPRESSAO)
        | not FATOR
    """
    global current_token, tabela, pilha_tipos

    if current_token['classification'] == 'Id\t\t':
        # Check if id in table
        has_id(current_token)

        #[SMT] coloca o tipo do identificador na pilha de tipos
        pilha_tipos.push(tabela.get_simbolo_tipo(current_token['token']))

        getSimbol()

        if not FATOR_DESAMBIGUIDADE():
            return False
        else:
            return True
    else:

        if current_token['classification'] == 'Inteiro\t\t':
            pilha_tipos.push('integer')
            getSimbol()
            return True

        if current_token['classification'] == 'Float\t\t':
            pilha_tipos.push('real')
            getSimbol()
            return True

        if current_token['token'] == 'true' or current_token['token'] == 'false':
            pilha_tipos.push('boolean')
            getSimbol()
            return True
        
        if current_token['token'] == '(':
            getSimbol()
            if not EXPRESSAO():
                return False
            
            if current_token['token'] == ')':
                getSimbol()
                return True
            else:
                print_error(')')
                return False
                
        if current_token ['token'] == 'not':
            getSimbol()
            if not FATOR():
                return False
    
    # special case:
    print_error("id or '('")
    return False

def FATOR_DESAMBIGUIDADE():
    """
    FATOR_DESAMBIGUIDADE
        (LISTA_DE_EXPRESSOES)
        | e
    """
    
    global current_token, tabela, pilha_tipos
    if current_token['token'] == '(':
        getSimbol()
        if not LISTA_DE_EXPRESSOES():
            return False
        if current_token['token'] == ')':
            getSimbol()
            return True

        else:
            print_error(")")
            return False
    else:
        return True # vazio

def LISTA_DE_EXPRESSOES():
    """
    LISTA_DE_EXPRESSOES :
	    EXPRESSAO LISTA_DE_EXPRESSOES_2
    """

    if not EXPRESSAO():
        return False

    if not LISTA_DE_EXPRESSOES_2():
        return False

    return True

def LISTA_DE_EXPRESSOES_2():
    """
    LISTA_DE_EXPRESSOES_2
        , EXPRESSAO LISTA_DE_EXPRESSOES_2
        | e
    """
    
    if current_token['token'] == ',':
        getSimbol()

        if not EXPRESSAO():
            return  False

        if not LISTA_DE_EXPRESSOES_2():
            return False

    else:
        return True # vazio
    
    return True

def EXPRESSAO():
    """
    EXPRESAO
        EXPRESSAO_SIMPLES EXPRESSAO_DESAMBIGUIDADE
    """
    if not EXPRESAO_SIMPLES() : return False
        
    if not EXPRESSAO_DESAMBIGUIDADE(): return False

    return True

def EXPRESSAO_DESAMBIGUIDADE():
    """
    e
	| OP_RELACIONAL EXPRESSAO_SIMPLES
    """
    
    global pilha_tipos, current_token

    if not OP_RELACIONAL():
        return True # vazio


    if not EXPRESAO_SIMPLES():
        return False

    #[SMT] verifica a pilha de tipos
    if not pilha_tipos.reduz_pct_relacional():
        sys.exit("Incompatibilidade de tipos. Linha: " + str(current_token['line']))
    
    return True

def EXPRESAO_SIMPLES():
    """
    EXPRESSAO_SIMPLES :
        TERMO EXPRESSAO_SIMPLES_2
        | SINAL TERMO EXPRESSAO_SIMPLES_2
    """
    
    if not TERMO():
        if not SINAL(): return False
        if not TERMO(): return False
        if not EXPRESSAO_SIMPLES_2(): return False
    
    else:
        if not EXPRESSAO_SIMPLES_2(): return False


    return True

def EXPRESSAO_SIMPLES_2 ():
    """
    EXPRESSAO_SIMPLES_2 : {
	    OP_ADITIVO TERMO EXPRESSAO_SIMPLES_2
	    | e
    """
    global current_token

    if not OP_ADITIVO():
        return True # vazio

    if not TERMO() : return False
    if not EXPRESSAO_SIMPLES_2() : return False

    verficar_operacao(current_token['token'])

    return True

def TERMO():
    """
    TERMO :
	    FATOR TERMO_2
    """
    if not FATOR(): return False
    if not TERMO_2(): return False

    return True

def TERMO_2():
    """
    TERMO_2 :{
        OP_MULTIPLICATIVO FATOR
        | e
    """
    global current_token

    if not OP_MULTIPLICATIVO():
        return True # vazio

    if not FATOR(): return False

    verficar_operacao(current_token['token'])

    return True