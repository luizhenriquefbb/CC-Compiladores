#!/usr/bin/python3
 # -*- coding: utf-8 -*- 

import sys

class Symbol:
    '''
    Símbolo.
    '''
    def __init__(self, simbolo, tipo):
        self.simbolo = simbolo  #o simbolo
        self.tipo = tipo    #tipo do símbolo

    def __repr__(self):
        return "("+str(self.simbolo) +", "+self.tipo+")"

class SymbolsTable:
    '''
    Tabela de símbolos.
    '''
    def __init__(self):
        self.marca = "$"    #marca de separação de escopos
        self.tabela = []    #tabela de símbolos

    def novo_escopo(self):
        '''
        Cria novo escopo.

        Adiciona na tabela o simbolo especial
        '''
        self.tabela.append(self.marca)

    def simbolo_no_escopo(self, simbolo):
        '''
        Procura e verifica se um símbolo já existe no escopo atual
        '''
        invert_tabela = self.tabela[::-1]   #inverte a tabela
        index_marca = invert_tabela.index(self.marca)  #pegar o índice da primeira ocorrência da marca

        for s in invert_tabela[:index_marca]:   #procura o símbolo no escopo atual
            if s.simbolo == simbolo:
                return True
        
        return False

    def push_simbolo(self, simbolo, tipo):
        '''
        Coloca um novo símbolo na tabela de símbolo
        '''
        if not self.simbolo_no_escopo(simbolo): #se o símbolo nãp existe no escopo
            self.tabela.append(Symbol(simbolo, tipo))   #adiciona o novo símbolo
            #print(self.tabela)
        else:
            sys.exit("Indentificador '" + simbolo + "' já no escopo!")  #se já existir o símbolo no escopo
    
    def pop_escopo(self):
        '''
        Remove os símbolos do escopo da tabela
        '''
        if len(self.tabela) == 1:
            self.tabela = []
            return

        invert_tabela = self.tabela[::-1]   #inverter a tabela
        index_marca = invert_tabela.index(self.marca)   #procurar a primeira aparição da marca
        invert_tabela = invert_tabela[index_marca + 1:] #pegar todos os valores a partir da última ocorrência da marca

        self.tabela = invert_tabela[::-1]   #inverte a tabela novamente

        #print(self.tabela)
    
    def simbolo_na_tabela(self, simbolo):
        '''
        Verifica se um símbolo está contído na tabela
        '''
        #print("<<<<<<<<<<<< Pesquisando "+simbolo)
        for value in self.tabela: #procura em toda tabela
            if value != self.marca:
                if value.simbolo == simbolo:
                    return True
        
        return False
    
    def set_tipo(self, tipo):
        '''
        Insere o tipo nos símbolos marcados com '.'
        '''
        for index, value in enumerate(self.tabela):
            if value != self.marca:
                if value.tipo == ".":
                    self.tabela[index].tipo =  tipo

        #print(self.tabela)

    def get_simbolo_tipo(self, simbolo):
        '''
        Retorna o tipo da última ocorrência do símbolo na tabela
        '''
        tipo = ''
        for value in self.tabela:
            if value != self.marca:
                if value.simbolo == simbolo:
                     tipo = value.tipo
        
        return tipo
