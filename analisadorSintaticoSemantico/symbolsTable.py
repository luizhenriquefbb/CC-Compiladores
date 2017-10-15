#!/usr/bin/python3

import sys

class Symbol:
    def __init__(self, simbolo, tipo):
        self.simbolo = simbolo
        self.tipo = tipo

    def __repr__(self):
        return "("+str(self.simbolo) +", "+self.tipo+")"

class SymbolsTable:
    def __init__(self):
        self.marca = "$"
        self.tabela = []

    def novo_escopo(self):
        self.tabela.append("$")
    
    def simbolo_no_escopo(self, simbolo):
        invert_tabela = self.tabela[::-1]
        index_marca = invert_tabela.index("$")

        for s in invert_tabela[:index_marca]:
            if s.simbolo == simbolo:
                return True
        
        return False

    def push_simbolo(self, simbolo, tipo):
        if not self.simbolo_no_escopo(simbolo):
            self.tabela.append(Symbol(simbolo, tipo))
            #print(self.tabela)
        else:
            sys.exit("Indentificador '" + simbolo + "' já no escopo!")
    
    def pop_escopo(self):
        if len(self.tabela) == 1:
            self.tabela = []
            return

        invert_tabela = self.tabela[::-1]
        index_marca = invert_tabela.index("$")
        invert_tabela = invert_tabela[index_marca + 1:]

        self.tabela = invert_tabela[::-1]

        #print(self.tabela)
    
    def simbolo_na_tabela(self, simbolo):
        #print("<<<<<<<<<<<< Pesquisando "+simbolo)
        for index, value in enumerate(self.tabela):
            if value != "$":
                if value.simbolo == simbolo:
                    return True
        
        return False
    
    def set_tipo(self, tipo):
        for index, value in enumerate(self.tabela):
            if value != "$":
                if value.tipo == ".":
                    self.tabela[index].tipo =  tipo
        #print(self.tabela)

    def get_simbolo_tipo(self, simbolo):
        for index, value in enumerate(self.tabela):
            if value != "$":
                if value.simbolo == simbolo:
                    return value.tipo
        
        return False
