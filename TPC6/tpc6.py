import ply.lex as lex

tokens = (
    'COMENTARIOML',
    'COMENTARIOSL',
    'VARIAVEL',
    'PARDIR',
    'PARESQ',
    'CHAVDIR',
    'CHAVESQ',
    'PONTOVIRG',
    'IGUAL',
    'MAIS',
    'MENOS',
    'VEZES',
    'DIV',
    'IGUALIGUAL',
    'MAIOR',
    'MAIORIGUAL',
    'MENOR',
    'MENORIGUAL',
    'DIF',
    'PARRDIR',
    'PARRESQ',
    'VIRGULA',
    'PONTOPONTO',
    'NUM',
    'INT',
    'PRINT',
    'FOR',
    'WHILE',
    'FUNCTION',
    'PROGRAM',
    'IN'
)

def t_COMENTARIOML(t):
    r'\/\*(\*(?!\/)|[^*])*\*\/'
    pass

def t_COMENTARIOSL(t):
    r'//.*\n'
    pass

t_PARDIR = r'\)'
t_PARESQ = r'\('
t_CHAVDIR = r'}'
t_CHAVESQ = r'{'
t_PONTOVIRG = r';'
t_IGUAL = r'='
t_MAIS = r'\+'
t_MENOS = r'-'
t_VEZES = r'\*'
t_DIV = r'/'
t_IGUALIGUAL = r'=='
t_MAIOR = r'>'
t_MAIORIGUAL = r'>='
t_MENOR = r'<'
t_MENORIGUAL = r'<='
t_DIF = r'!='
t_PARRDIR = r'\]'
t_PARRESQ = r'\['
t_VIRGULA = r','
t_PONTOPONTO = r'\.\.'

def t_NUM(t):
    r'-?\d+'
    t.value = int(t.value)
    return t

def t_INT(t):
    r'int'
    return t

def t_PRINT(t):
    r'print\(.*\)'
    return t

def t_FOR(t):
    r'for'
    return t

def t_WHILE(t):
    r'while'
    return t

def t_IN(t):
    r'in'
    return t

def t_FUNCTION(t):
    r'function\s\w+\(.*\)'
    return t

def t_PROGRAM(t):
    r'program\s\w+'
    return t

def t_VARIAVEL(t):
    r'\w+'
    return t


t_ignore = " \n\t"

def t_error(t):
    print(f"Caracter Ilegal {t.value[0]}")
    t.lexer.skip(1)

lexer = lex.lex()


data = '''
/* factorial.p
-- 2023-03-20 
-- by jcr
*/

int i;

// Função que calcula o factorial dum número n
function fact(n){
  int res = 1;
  while res > 1 {
    res = res * n;
    res = res - 1;
  }
}
// Programa principal
program myFact{
  for i in [1..10]{
    print(i, fact(i));
  }
}
'''


lexer.input(data)

while tok := lexer.token():
    print(tok)