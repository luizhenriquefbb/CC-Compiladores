#!/usr/bin/python3
 # -*- coding: utf-8 -*- 

import sys

class TypesStack:
    '''
    Pilha de tipos.
    '''
    def __init__(self):
        self.pilha = [] #pilha de tipos 
    
    def push(self, tipo):
        '''
        Colocar um novo tipo na pilha
        '''
        self.pilha.append(tipo)
    
    def pop(self):
        '''
        Remover o tipo no topo da pilha
        '''
        self.pilha.pop(-1)
    
    def reduz_pct(self):
        '''
        Reduz a pilha de tipos para operações aritiméticas.
        '''
        try:
            topo = self.pilha[-1]
            subTopo = self.pilha[-2]
        except IndexError:
            return False

        if topo == "integer" and subTopo == "integer":
            self.atualiza_pct("integer")

        elif topo == "integer" and subTopo == "real":
            self.atualiza_pct("real")

        elif topo == "real" and subTopo == "integer":
            self.atualiza_pct("real")

        elif topo == "real" and subTopo == "real":
            self.atualiza_pct("real")

        else:
            print("Os tipos '"+ topo +"' e '"+ subTopo +"' não são compatíveis")
            return False

        return True
    
    def reduz_pct_relacional(self):
        '''
        Redução da pilha de tipos para operações relacionais.
        '''
        try:
            topo = self.pilha[-1]
            subTopo = self.pilha[-2]
        except IndexError:
            return False

        tipos = ["integer","real"]

        if topo in tipos and subTopo in tipos:  #apenas para valores numéricos
            self.atualiza_pct("boolean")

        else:
            print("Os tipos '"+ topo +"' e '"+ subTopo +"' não são compatíveis")
            return False

        return True
    
    def reduz_pct_logico(self):
        '''
        Redução da tabela de tipos para openrações lógicas.
        '''

        try:
            topo = self.pilha[-1]
            subTopo = self.pilha[-2]
        except IndexError:
            return False

        if topo == "boolean" and subTopo == "boolean":  #apenas para tipos booleanos 
            self.atualiza_pct("boolean")
            return True
        
        return False

    def atualiza_pct(self, tipo):
        '''
        Atualiza o topo da tabela de tipos.
        '''
        self.pilha.pop()
        self.pilha.pop()
        self.push(tipo)

    def topo(self):
        '''
        Retorna o topo da pilha
        '''
        return self.pilha[-1]

    def __str__(self):
        tostring = ''

        for el in self.pilha:
            tostring += el+'\n'

        return tostring
