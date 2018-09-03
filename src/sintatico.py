from util import *
import sys

current_token = {
    'token': '',
    'classification': '',
    'line': ''
}

def sintatico (_input):
    global current_token, tokens

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
    global current_token
    
    if line == None:
        line = current_token['line']

    # print ("erro: expected: '"+ expected +"' at line " + str(line)+". Found '"+current_token['token']+"'", end='\r') #python 3
    sys.stdout.write('\r'+"erro: expected: '"+ expected +"' at line " + str(line)+". Found '"+current_token['token']+"'")
    sys.stdout.write("\033[K")
    sys.stdout.flush() #python 2

def getSimbol():
    global current_token
    current_token = tokens.pop(0)
    # return current_token


def PROGRAMA():
    """
    PROGRAMA 
        program id;
        DECLARACOES_VARIAVEIS
        DECLARACOES_DE_SUBPROGRAMAS
        COMANDO_COMPOSTO
        .
    """
    global current_token

    if current_token['token'] == 'program':
        getSimbol()
        if current_token['classification'] == 'Id\t\t':
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
    global current_token

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
    global current_token
    
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
    global current_token

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
    global current_token

    if current_token['classification'] == 'Id\t\t':
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
    global current_token
    if current_token['token'] == ',':
        getSimbol()
        if current_token['classification'] == 'Id\t\t':
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
    global current_token

    if current_token['token'] == 'integer' or current_token['token'] == 'real' or current_token['token'] == 'boolean':
        getSimbol()
        return True

    else:
        print_error("'inteiro/real/boolean")
        return False


def DECLARACOES_DE_SUBPROGRAMAS():
    """
    DECLARACOES_DE_SUBPROGRAMAS 
        | DECLARACOES_DE_SUBPROGRAMAS_2
    """

    global current_token

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

    global current_token

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

    global current_token
    
    if current_token['token'] == 'procedure':
        getSimbol()
        if current_token['classification'] == 'Id\t\t':
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
    global current_token

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
    global current_token

    if current_token['token'] == ';':
        getSimbol()

        if LISTA_DE_IDENTIFICADORES() == False:
            return False

        if current_token['token'] == ':':
            getSimbol()

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
    global current_token

    if current_token['token'] == 'begin':
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
    if current_token['token'] == ";":
        getSimbol()
        if current_token['token'] == 'end':
            getSimbol()

        else:
            print_error("end")
            return False
    else:
        if current_token['token'] == 'end':
            getSimbol()

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

    global current_token

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
    global current_token

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

    global current_token

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
    global current_token
    if current_token['classification'] == 'Id\t\t':
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

    global current_token

    if current_token['classification'] == 'Id\t\t':
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
    global current_token
    
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

    global current_token

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

    global current_token
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

    global current_token
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

    global current_token
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
    global current_token

    if current_token['classification'] == 'Id\t\t':
        getSimbol()
        if not FATOR_DESAMBIGUIDADE():
            return False
        else:
            return True
    else:

        if current_token['classification'] == 'Inteiro\t\t':
            getSimbol()
            return True

        if current_token['classification'] == 'Float\t\t':
            getSimbol()
            return True

        if current_token['classification'] == 'true' or current_token['token'] == 'false':
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
    
    global current_token
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
    if not OP_RELACIONAL():
        return True # vazio

    if not EXPRESAO_SIMPLES():
        return False

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

    if not OP_ADITIVO():
        return True # vazio

    if not TERMO() : return False
    if not EXPRESSAO_SIMPLES_2() : return False

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

    if not OP_MULTIPLICATIVO():
        return True # vazio

    if not FATOR(): return False

    return True