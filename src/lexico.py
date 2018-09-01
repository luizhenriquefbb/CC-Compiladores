from util import *

current_token = {
    'token': '',
    'classification': '',
    'line': ''
}

def lexico ():
    global current_token

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

    print ("erro: expected: '"+ expected +"' at line " + str(line)+". Found '"+current_token['token']+"'")

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
                    getSimbol()
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

    # getSimbol()
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


def COMANDO_COMPOSTO():
    """
    COMANDO_COMPOSTO
        begin
        COMANDOS_OPCIONAIS
        end
    """
    global current_token

    if current_token['token'] == 'begin':
        getSimbol()
        if COMANDOS_OPCIONAIS() == False:
            return False

        if current_token['token'] == 'end':
            getSimbol()
            return True
        else:
            print_error('end')
            return False

    else:
        print_error('begin')
        return False


    # getSimbol()
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
        getSimbol()
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
            return False

        if LISTA_DE_COMANDOS_2() == False:
            return False

    else:
        return True #vazio

def COMANDO():
    """
    COMANDO :
        VARIAVEL := EXPRESSAO
        | ATIVACAO_DE_PROCEDIMENTO
        | COMANDO_COMPOSTO
        | if EXPRESSAO then COMANDO PARTE_ELSE
        | while EXPRESSAO do COMANDO
    """
    tokens = []
    return True