import sys
import json
import ply.lex as lex

tokens = (
    'AMOUNT',
    'LIST',
    'EXIT',

    'COIN',
    'EUR',
    'CENT',
    'DOT',

    'SELECT', 
    'CODE'
)

# Define lexer states
states = (
    ('COIN', 'exclusive'),
    ('SELECT', 'exclusive')
)

######################################### Auxiliary functions

def fact_amount(money):
    coins = [200, 100, 50, 20, 10, 5, 2, 1]
    ans = []

    res = money
    for m in coins:
        qtd = res // m
        if qtd > 0:
            if m >= 100:
                name = f"{m//100}e"
            else:
                name = f"{m}c"
            ans.append(f"{qtd}x {name}")
            res -= qtd * m

    if not ans:
        return "0c"
    elif len(ans) == 1:
        return ans[0]
    else:
        return ', '.join(ans[:-1]) + ' e ' + ans[-1]


######################################### INITIAL STATE

def t_AMOUNT(t):
    r'SALDO'
    print(f'Saldo = {t.lexer.saldo}c')

    return t

def t_LIST(t):
    r'LISTAR'

    print("cod | nome                      | quantidade | preço")
    print("----------------------------------------------------")
    for item in stock:
        print(f"{item['cod']:3} | {item['nome']:<25} | {item['quant']:10} | {item['preco']:.2f}")
    return t

def t_EXIT(t):
    r'SAIR'
    print('Pode retirar o troco: '+fact_amount(t.lexer.saldo))
    print('Até à próxima')
    return t

def t_newline(t):
    r'\n'
    t.lexer.lineno += len(t.value)
    
t_ignore = ' \t'

def t_error(t):
    print(f"Carácter ilegal {t.value[0]}")
    t.lexer.skip(1)

######################################### COIN STATE

def t_COIN(t):
    r'MOEDA'
    t.lexer.code_start = t.lexer.lexpos
    t.lexer.begin('COIN')
    return t

def t_COIN_EUR(t):
    r'(1e|2e)'
    t.value = int(t.value[:-1])*100
    t.lexer.saldo += t.value
    return t

def t_COIN_CENT(t):
    r'(5c|50c|10c|20c)'
    t.value = int(t.value[:-1])
    t.lexer.saldo += t.value
    return t

def t_COIN_DOT(t):
    r'\.'
    print(f'Saldo = {t.lexer.saldo}c')
    t.lexer.begin('INITIAL')
    return t

t_COIN_ignore = ' \t\n,'

def t_COIN_error(t):
    print(f"Error in state COIN: {t.value[0]!r}")
    t.lexer.skip(1)

######################################### SELECT STATE

def t_SELECT(t):
    r'SELECIONAR'
    t.lexer.code_start = t.lexer.lexpos
    t.lexer.begin('SELECT')
    return t

def t_SELECT_CODE(t):
    r'[A-Z]+\d+'

    for i in range(len(t.lexer.stock)):
        if t.lexer.stock[i]['cod'] == t.value:
            prod = t.lexer.stock[i]

    if prod['quant'] > 0 and prod['preco']*100 <= t.lexer.saldo:
        prod['quant'] -= 1
        t.lexer.saldo -= prod['preco']*100

        print(f"Pode retirar o produto dispensado \"{prod['nome']}\"")
        print(f'Saldo: {t.lexer.saldo}c')
    elif prod['preco']*100 > t.lexer.saldo:
        print("Saldo insuficiente para satisfazer o seu pedido, cry about it")
        print(f'Saldo: {t.lexer.saldo}; Pedido={prod["preco"]}c')
    else:
        print("Produto não disponível")

    t.lexer.begin('INITIAL')
    return t

t_SELECT_ignore = ' \t\n,'

def t_SELECT_error(t):
    print(f"Error in state SELECT: {t.value[0]!r}")
    t.lexer.skip(1)

#########################################

# Stock setup
try:
    with open("stock.json", "r", encoding="utf-8") as f:
        stock = json.load(f)
except FileNotFoundError:
    stock = [{"cod": "A23", "nome": "água 0.5L", "quant": 8, "preco": 0.7}]

lexer = lex.lex()
lexer.stock = stock
lexer.saldo = 0

print(f"Stock carregado, Estado atualizado.")
print("Bom dia. Estou disponível para atender o seu pedido.")

# Read input
for linha in sys.stdin:
    lexer.input(linha)
    for tok in lexer:
        tok
