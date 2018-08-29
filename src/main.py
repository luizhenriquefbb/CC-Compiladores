import re
from util import *


def main(input_string):

    input_string+=' '
    

    # List of key words
    # lista de palavras chaves
    reserved_words = build_list_of_reserved_words()
    ignored_words = build_list_of_ignored()
    relationals = build_list_of_relationals()
    operators = build_list_of_operators()
    attributers = build_list_of_attributers()
    delimiters = build_list_of_delimiters()

    # line counter
    # Contador de linhas
    number_of_lines = 1

    # true when inside of a comment
    # verifica se o comentario esta aberto
    comment_is_open = False
    line_comment = False

    # string index
    # index da string que vai sendo incrementada
    current_index = 0

    # palavra que vai ser formando caractere a caractere
    word = ''

    # expressao regular para detectar se uma palavra pode ser uma variavel
    variable_reg = re.compile(r"[A-Za-z_]+[A-Za-z0-9_]*$")
    
    # expressao regular para detectar se uma palavra pode ser um inteiro
    integer_reg = re.compile(r"[0-9]+$")
    
    # expressao regular para detectar se uma palavra pode ser um float
    float_reg = re.compile(r"[0-9]+[\.]{0,1}[0-9]*$")
    # float_reg = re.compile(r"[0-9]+\.[0-9]*$")


    # lista de possibilidades que uma palavra pode ter.
    # A medida que a PALAVRA (word) vai sendo formada, os itens da lista vai sendo removido
    list_of_classifications = [
        "Palavras reservadas",
        "Ser ignorada",
        "Relacional\t",
        "Operador\t",
        "Atribuidor\t",
        "Delimitador\t",
        "Inteiro\t\t",
        "Float\t\t",
        "Variavel\t",
        "Numero 3D"
    ]


    current_possibilities = list_of_classifications[:]

    # read all char
    # Ler todos os caracteres, um a um
    while current_index < len(input_string):
        # remove inadequate categories
        # Vai removendo todas as categorias em que a palvra nao pode ser ate so sobrar uma
        while len(current_possibilities) > 1:

            # condicao para evitar nao ler alem da string de entrada
            if current_index < len(input_string):
                
                if input_string[current_index] == '\n':
                    number_of_lines += 1
                    current_index += 1
                    line_comment = False
                    continue

                # palavras a serem ignoradas
                elif input_string[current_index] in ignored_words:
                    current_index += 1
                    continue

                # Comentario de linha
                if input_string[current_index] == '/' and input_string[current_index+1] == '/':
                    current_index += 2
                    line_comment = True
                    continue


                # Comentario
                if input_string[current_index] == '{' and not comment_is_open:
                    add_token('{', "comentario aberto", number_of_lines)
                    current_index += 1
                    comment_is_open = True
                    continue

                if input_string[current_index] == '}' and comment_is_open:
                    add_token('}', "comentario fechado", number_of_lines)
                    current_index += 1
                    comment_is_open = False
                    continue
                
                if comment_is_open or line_comment:
                    current_index += 1
                    continue
                
                # coloca o caractere na "palavra"
                word+=input_string[current_index]


                # numero 3d
                
                # ███╗   ██╗██╗   ██╗███╗   ███╗███████╗██████╗  ██████╗     ██████╗ ██████╗ 
                # ████╗  ██║██║   ██║████╗ ████║██╔════╝██╔══██╗██╔═══██╗    ╚════██╗██╔══██╗
                # ██╔██╗ ██║██║   ██║██╔████╔██║█████╗  ██████╔╝██║   ██║     █████╔╝██║  ██║
                # ██║╚██╗██║██║   ██║██║╚██╔╝██║██╔══╝  ██╔══██╗██║   ██║     ╚═══██╗██║  ██║
                # ██║ ╚████║╚██████╔╝██║ ╚═╝ ██║███████╗██║  ██║╚██████╔╝    ██████╔╝██████╔╝
                # ╚═╝  ╚═══╝ ╚═════╝ ╚═╝     ╚═╝╚══════╝╚═╝  ╚═╝ ╚═════╝     ╚═════╝ ╚═════╝ 
                #                                                                            
                if can_be_3d(word) and "Numero 3D" in current_possibilities:
                    # concatena ate nao puder ser mais float
                    while can_be_3d(word) and current_index < len(input_string):
                        
                        current_index+=1
                        word+=input_string[current_index]
                    
                    # remove o caractere que quebrou pra nao imprimir-lo
                    current_index-=1
                    word = word[:-1]

                    if can_be_3d_final(word):
                        current_possibilities = ["Numero 3D"]
                    else:
                        try:
                            current_possibilities = [
                                "Palavras reservadas",
                                "Ser ignorada",
                                "Relacional\t",
                                "Operador\t",
                                "Atribuidor\t",
                                "Delimitador\t",
                                "Inteiro\t\t",
                                "Float\t\t",
                                "Variavel\t"
                            ]

                            current_index-=len(word)-1
                            word = input_string[current_index]
                        except ValueError:
                            pass
                

                else:
                    try:
                        current_possibilities.remove("Numero 3D")
                    except ValueError:
                        pass





                # verifica classe a classe
                if not can_be_substring_of(word, reserved_words):
                    try:
                        current_possibilities.remove("Palavras reservadas")
                    except ValueError:
                        pass
                if not can_be_substring_of(word, ignored_words):
                    try:
                        current_possibilities.remove("Ser ignorada")
                    except ValueError:
                        pass
                if not can_be_substring_of(word, relationals):
                    try:
                        current_possibilities.remove("Relacional\t")
                    except ValueError:
                        pass
                if not can_be_substring_of(word, operators):
                    try:
                        current_possibilities.remove("Operador\t")
                    except ValueError:
                        pass
                if not can_be_substring_of(word, attributers):
                    try:
                        current_possibilities.remove("Atribuidor\t")
                    except ValueError:
                        pass
                if word not in delimiters:
                    try:
                        current_possibilities.remove("Delimitador\t")
                    except ValueError:
                        pass
                
                # remove variable possibility
                if not variable_reg.match(word) and "Variavel\t" in current_possibilities:
                    current_possibilities.remove("Variavel\t")

                # Float
                if float_reg.match(word):
                    # concatena ate nao puder ser mais float
                    while float_reg.match(word) and current_index < len(input_string):
                        
                        current_index+=1
                        word+=input_string[current_index]
                    
                    # remove o caractere que quebrou pra nao imprimir-lo
                    current_index-=1
                    word = word[:-1]
                    current_possibilities = ["Float\t\t"]


                else:
                    try:
                        current_possibilities.remove("Float\t\t")
                    except ValueError:
                        pass
               
               
                # inteiro
                if integer_reg.match(word):
                    # concatena ate nao puder ser mais int
                    while integer_reg.match(word) and current_index < len(input_string):
                        
                        current_index+=1
                        word+=input_string[current_index]
                    
                    # remove o caractere que quebrou pra nao imprimir-lo
                    current_index-=1
                    word = word[:-1]
                    current_possibilities = ["Inteiro\t\t"]


                else:
                    try:
                        current_possibilities.remove("Inteiro\t\t")
                    except ValueError:
                        pass


                # Special cases:
                 # do not break string until does not match with variable
                # se so pode ser uma variavel, continuar concatenando caracteres ate nao puder ser mais uma variavel
                if "Variavel\t" in current_possibilities:
                    while variable_reg.match(word) and current_index < len(input_string):
                        current_index+=1
                        # tratamento com \n. Evitar colocar \n em word
                        if current_index < len(input_string) and input_string[current_index] <> '\n':
                            word+=input_string[current_index]
                        else:
                            break

                    # remove o caractere que quebrou a E.R
                    if current_index < len(input_string) and input_string[current_index] <> '\n':
                        word = word[:-1]
                    else:
                       pass

                    current_index-=1
                    

                    current_possibilities = ["Variavel\t"]

                # if word is a key word, desconsider word be a variable
                if "Variavel\t" in current_possibilities:
                    # word match exactly with a key word
                        
                        
                    if word in reserved_words:
                        current_possibilities = ["Palavras reservadas"]
                    if word in ignored_words:
                        current_possibilities = ["Ser ignorada"]
                    if word in relationals:
                        current_possibilities = ["Relacional\t"]
                    if word in operators:
                        current_possibilities = ["Operador\t"]
                    if word in attributers:
                        current_possibilities = ["Atribuidor\t"]
                    if word in delimiters:
                        current_possibilities = ["Delimitador\t"]



                # :
                if ':' == word and current_index < len(input_string) and '=' is not input_string[current_index+1]:
                    current_possibilities = ["Delimitador\t"]

            else:
                break
                
            if len(current_possibilities) > 1:
                current_index += 1
        # end len(current_possibilities) > 1



        # Error!!
        if len(current_possibilities) == 0:
            add_token(word, "erro\t\t", number_of_lines)

        # found !!
        if len(current_possibilities) == 1:
            add_token(word, current_possibilities[0], number_of_lines)
            
        # find next token
        word = ''
        current_possibilities = list_of_classifications[:]
        current_index += 1
    
    # End read all chars

    if comment_is_open:
        print "erro!!: comentario nao fechado"

"""
    This function receive a word and a list. Its checks if the word can be in list.
    Example: word = "casa" and list = ["casa", "predio"]
    "cas" can be "casa", So return true

    --------

    Essa funcao recebe uma PALAVRA e uma LISTA. Ela verifica se a palavra pode estar na lista.

    Exemplo: palavra = "cas" e lista = ["casa", "predio"]
    "cas" pode ser "casa", entao retorna TRUE

 """
def can_be_substring_of(word, a_list):
    
    # Casos que interferem no regex
    word = word.replace("*", "\\*")
    word = word.replace("+", "\\+")
    word = word.replace(".", "\\.")

    matches = []
    for element in a_list:
        pattern = re.compile(word+".*")
        if pattern.match(element):
            matches.append(element)
    
    if len(matches) > 0 :
        return True
    else:
        return False

def can_be_3d(word):
    '''
    Condicao para continuar concatenando caracteres na string
    '''
    case1 = re.compile(r"[0-9]+[\.]{0,1}[0-9]*$")
    case2 = re.compile(r"[0-9]+[\.]{0,1}[0-9]*x$")
    case3 = re.compile(r"[0-9]+[\.]{0,1}[0-9]*x[0-9]+[\.]{0,1}[0-9]*$")
    case4 = re.compile(r"[0-9]+[\.]{0,1}[0-9]*x[0-9]+[\.]{0,1}[0-9]*y$")
    case5 = re.compile(r"[0-9]+[\.]{0,1}[0-9]*x[0-9]+[\.]{0,1}[0-9]*y[0-9]+[\.]{0,1}[0-9]*$")
    case6 = re.compile(r"[0-9]+[\.]{0,1}[0-9]*x[0-9]+[\.]{0,1}[0-9]*y[0-9]+[\.]{0,1}[0-9]*z$")

    if case1.match(word):
        return True
    if case2.match(word):
        return True
    if case3.match(word):
        return True
    if case4.match(word):
        return True
    if case5.match(word):
        return True
    if case6.match(word):
        return True

    return False


def can_be_3d_final(word):

    case6 = re.compile(r"[0-9]+[\.]{0,1}[0-9]*x[0-9]+[\.]{0,1}[0-9]*y[0-9]+[\.]{0,1}[0-9]*z$")

    
    if case6.match(word):
        return True

    return False




if __name__ == '__main__':
    # input_string = 'if \n43teste var \n uo{qweh 322}23 j23jn234 program'
    input_string = (
        "program teste; {programa exemplo}\n"+
        "var\n"+
        "valor1: integer;\n"+
        "valor2: real;\n"+
        "begin\n"+
        "valor1 := 10 *;\n"+
        "end.\n"+
        "90 89.7 12   & = #\n"+
        "variavel var1\n"+
        "// isso eh um comentario de linha\n"+
        "0.3x2.0y4.9z"+
        "12.34.56"+
        "")

    print_row("TOKEN", "CLASSIFICACAO", "LINHA")
    main(input_string)
    print("the end")
