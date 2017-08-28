
import sys,os

sys.path.append("/".join(os.getcwd().split("/")[:-1])+"/analisador-lexico")

import LexicalAnalyzer

class SyntaxAnalyzer():
    def __init__(self, list_tokens):
        self.list_tokens = list_tokens
        self.current =  None
        self.index = 0

    def next(self):
        if self.index < len(self.list_tokens):
            self.current = self.list_tokens[self.index]
            self.index += 1
            return self.current
        return None
    
    def stop(self, text):
        sys.exit(str(self.current)+"\n"+text)

    def startAnalysis(self):
        if self.next().word == "program":
            if self.next().lex == "Identificador":
                if self.next().word == ";":
                    if self.declaracoes_variaveis():
                        if self.declaracoes_subprogramas():
                            if not self.comando_composto():
                                self.stop("Comando compostos inválidos")
                        else:
                            self.stop("Declarações de subprogramas inválido")
                    else:
                        self.stop("Declaração de variáveis inválida")
                    if self.next().word == ".":
                        return True
                    else:
                        return False
                else:
                   self.stop("Erro: Falta o ';' após o nome do programa")
            else:
                self.stop("Erro: O programa está sem nome")
        else:
            self.stop("Erro: O programa não começou com 'program'")

    def declaracoes_variaveis(self):
        if self.next().word == "var":
            return self.lista_declaracoes_variaveis()
        else:
            self.index -= 1
            return True
    
    def lista_declaracoes_variaveis(self):
        if self.lista_de_identificadores():
            if self.next().word == ":":
                if self.tipo():
                    if self.next().word == ";":
                        return self.lista_declaracoes_variaveis_ln()
                    else:
                        self.stop("O ';' não enontrado")
                else:
                    self.stop("Tipo inválido")
            else:
                self.stop("O ':' não foi encontrado")
        return True
    
    def lista_declaracoes_variaveis_ln(self):
        if self.lista_de_identificadores():
            if self.next().word == ":":
                if self.tipo():
                    if self.next().word == ";":
                        return self.lista_declaracoes_variaveis_ln()
                    else:
                        self.stop("O ';' não enontrado")
                else:
                    self.stop("Tipo inválido")
            else:
                self.stop("O ':' não foi encontrado")
        return True
    
    def lista_de_identificadores(self):
        if self.next().lex == "Identificador":
            return self.lista_de_identificadores_ln()
        else:
            self.stop("Identificador inválido")
    
    def lista_de_identificadores_ln(self):
        if self.next().word == ",":
            if self.next().lex == "Identificador":
                return lista_de_identificadores_ln()
            else:
                self.stop("Era esperado um identificador")
        else:
            self.index -= 1
            return True

    def tipo(self):
        if self.next().word == "integer":
            return True
        elif self.next().word == "real":
            return True
        elif self.next().word == "boolean":
            return True
        
        return False

    def declaracoes_subprogramas(self):
        return self.declaracoes_subprogramas_ln()
    
    def declaracoes_subprogramas_ln(self):
        if self.declaracao_subprograma():
            if self.next().word == ";":
                return self.declaracoes_subprogramas_ln()
            else:
                self.stop("Declaração de subprograma sem ';'")
        else:
            return True
    
    def declaracao_subprograma(self):
        if self.next().word == "procedure":
            if self.next().lex == "Identificador":
                if self.argumentos():
                    if self.next().word == ";":
                        if self.declaracoes_variaveis():
                            if self.declaracoes_subprogramas():
                                if self.comando_composto():
                                    return True
                                else:
                                    self.stop("Comando composto inválido")
                            else:
                                self.stop("Declaração de subprogramas inválido")
                        else:
                            self.stop("Declaração de variáveis inválida")
                    else:
                        self.stop("O ';' era esperado, mas não foi encontrador")
                else:
                    self.stop("Argumentos inválidos")
            else:
                self.stop("Procedure sem identificador")
        else:
            self.index -= 1
            return False
        
    def argumentos(self):
        if self.next().word == "(":
            if self.lista_de_parametros():
                if self.next.word() == ")":
                    return True
                else:
                    self.stop("O '(' não foi fechado")
            else:
                self.stop("Parâmetros inválidos")
        else:
            self.index -= 1
            return True
    
    def lista_de_parametros(self):
        if self.lista_de_identificadores:
            if self.next().word == ":":
                if self.tipo():
                    return self.lista_de_parametros_ln()
                else:
                    self.stop("Um tipo era esperado")
            else:
                self.stop("O ':' era esperado")
        else:
            self.stop("Identificador inválido")

    def lista_de_parametros_ln(self):
        if self.next().word == ";":
            if self.lista_de_identificadores:
                if self.tipo():
                    return self.lista_de_parametros_ln()
                else:
                    self.stop("Um tipo era esperado")
            else:
                self.stop("Identificador inválido")
        else:
            self.index -= 1
            return True
############################

if __name__ == "__main__":
     with open(sys.argv[1],"r") as program:
        lex = LexicalAnalyzer.LexicalAnalyzer()
        syn = SyntaxAnalyzer(lex.analyze(program.read()))
        syn.startAnalysis()