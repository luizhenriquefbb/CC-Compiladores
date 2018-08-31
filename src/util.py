tokens = []

def build_list_of_reserved_words():
    return [
        "token",
        "program",
        "var",
        "integer",
        "real",
        "boolean",
        "procedure",
        "begin",
        "end",
        "if",
        "then",
        "else",
        "while",
        "do",
        "not"
    ]

def build_list_of_ignored():
    return[
        ' ',
        '\t',
        # '\n', # REMEMBER COUNT LINES!!
        '\r'
    ]

def build_list_of_relationals():
    return [
        "=",
        "<",
        ">",
        "<=",
        ">=",
        "<>"
    ]

def build_list_of_operators():
    return [
        "+",
        "\+",
        "-",
        "or",
        "*",
        "\*",
        "/",
        "and"
    ]

def build_list_of_attributers():
    return [
        ":="
    ]

def build_list_of_delimiters():
    return [
        ".",
        "\.",
        ",",
        ":",
        ";"
    ]

def print_row(token, classification, line):
    if token is not '':
        s = '\t\t'
        print s.join([token, classification, str(line)])

def add_token(token, classification, line):
    tokens.append({'token': token, 'classification':classification, 'line':line})
    print_row(token, classification, line)