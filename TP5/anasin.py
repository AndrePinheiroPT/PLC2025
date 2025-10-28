from analex import lexer

# GRAMMAR:
# G1: Exp   -> INT ExpR
# G2:        | '(' Exp ')' ExpR
# G3: ExpR  ->
# G4:        | OP Exp

token_atual = ('Erro', '', 0, 0)

def erro_sintatico(token):
    print(f"Erro de sintaxe! Token inesperado: {token}")

def consome(tipo_esperado):
    global token_atual
    if token_atual.type == tipo_esperado:
        token_atual = lexer.token()
    else:
        erro_sintatico(token_atual)

def reconhece_ExpR():
    global token_atual

    if token_atual is None:
        print("Derivando G3: ExpR -> epsilon")
        print("Reconhecido G3: ExpR -> epsilon")
        return

    if token_atual.type == 'OP':
        print("Derivando G4: ExpR -> OP Exp")
        consome('OP')
        reconhece_Exp()
        print("Reconhecido G4: ExpR -> OP Exp")

    elif token_atual.type == 'PF': 
        print("Derivando G3: ExpR -> epsilon")
        print("Reconhecido G3: ExpR -> epsilon")

    else:
        erro_sintatico(token_atual)

def reconhece_Exp():
    global token_atual

    if token_atual.type == 'INT':
        print("Derivando G1: Exp -> INT ExpR")
        consome('INT')
        reconhece_ExpR()
        print("Reconhecido G1: Exp -> INT ExpR")

    elif token_atual.type == 'PA':
        print("Derivando G2: Exp -> '(' Exp ')' ExpR")
        consome('PA')
        reconhece_Exp()
        consome('PF')
        reconhece_ExpR()
        print("Reconhecido G2: Exp -> '(' Exp ')' ExpR")

    else:
        erro_sintatico(token_atual)

def RParser(codigo):
    global token_atual
    lexer.input(codigo)
    token_atual = lexer.token()
    reconhece_Exp()
    print("Análise concluída com sucesso!")
