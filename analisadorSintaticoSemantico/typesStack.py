#!/usr/bin/python3

class TypesStack:
    def __init__(self):
        self.pilha = []
    
    def push(self, tipo):
        self.pilha.append(tipo)
    
    def pop(self):
        self.pilha.pop(-1)
    
    def reduz_pct(self):
        topo = self.pilha[-1]
        subTopo = self.pilha[-2]

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
        topo = self.pilha[-1]
        subTopo = self.pilha[-2]
        tipos = ["integer","real"]

        if topo in tipos and subTopo in tipos:
            self.atualiza_pct("boolean")

        else:
            print("Os tipos '"+ topo +"' e '"+ subTopo +"' não são compatíveis")
            return False

        return True
    
    def reduz_pct_logico(self):
        topo = self.pilha[-1]
        subTopo = self.pilha[-2]

        if topo == "boolean" and subTopo == "boolean":
            self.atualiza_pct("boolean")
            return True
        
        return False

    def atualiza_pct(self, tipo):
        self.pilha.pop()
        self.pilha.pop()
        self.push(tipo)

    def topo(self):
        return self.pilha[-1]
