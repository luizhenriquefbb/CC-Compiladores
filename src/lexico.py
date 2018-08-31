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
                    return True

                else:
                    print ("erro: expected: '.' at line " + str(current_token['line']))
                    return False
                
                
            else:
                print ("erro: expected: ';' at line " + str(current_token['line']))
                return False
        else:
            print ("erro: expected: 'id' at line " + str(current_token['line']))
            return False
    else:
        print ("erro: expected: 'program' at line " + str(current_token['line']))
        return False
                
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
        getSimbol() # vazio

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
            print ("erro: expected: ';' at line " + str(current_token['line']))
            return False

    else:
        print ("erro: expected: ':' at line " + str(current_token['line']))
        return False

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
        getSimbol()
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
            print ("erro: expected: ';' at line " + str(current_token['line']))
            return False

    else:
        print ("erro: expected: ':' at line " + str(current_token['line']))
        return False


    return True


def LISTA_DE_IDENTIFICADORES():
    """
    LISTA_DE_IDENTIFICADORES 
        id LISTA_DE_IDENTIFICADORES_2
    """
    global current_token

    if current_token['classification'] == 'Id\t\t':
        getSimbol()
        if not LISTA_DECLARACOES_VARIAVEIS_2():
            return False


    else:
        print("error: expected 'id' at line "+ str(current_token['line']))
        return False


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
            if not LISTA_DE_IDENTIFICADORES_2():
                return False
        else:
            print("error: expected 'id' at line "+ str(current_token['line']))
            return False
    else:
        getSimbol()
        return True # vazio

    getSimbol()
    return True


def TIPO():
    """
    TIPO 
        integer
        | real
        | boolean
    """
    global current_token

    if current_token['token'] == 'inteiro' or current_token['token'] == 'real' or current_token['token'] == 'boolean':
        getSimbol()
        return True

    else:
        print("Error: expected 'inteiro/real/boolean, at line "+ str(current_token['line']))
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
        getSimbol()
        return True

def DECLARACOES_DE_SUBPROGRAMAS_2():
    """
    DECLARACOES_DE_SUBPROGRAMAS_2 
        DECLARACAO_DE_SUBPROGRAMA; DECLARACOES_DE_SUBPROGRAMAS_2
        | e
    """

    global current_token

    if not DECLARACAO_DE_SUBPROGRAMA():
        getSimbol()
        return True # vazio

    else:
        if current_token['token'] == ';':
            getSimbol()
            
            if not DECLARACOES_DE_SUBPROGRAMAS_2():
                return False

            
        else:
            print("Error: expected ';' at line "+ str(current_token['line']))
            return False

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
                print("Error: expected ';' at line "+ str(current_token['line']))
                return False

        else:
            print("Error: expected 'id' at line "+ str(current_token['line']))
            return False
    else:
        print("Error: expected 'procedure' at line "+ str(current_token['line']))
        return False



    return True


def ARGUMENTOS():
    """
    ARGUMENTOS 
        (LISTA_DE_PARAMETROS)
        | e
    """

    pass