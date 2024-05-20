import re
from tabulate import tabulate

test = open("Archivo.txt", "r")
lines = test.read().split(sep="\n")

res_words = {
    "programa": -1,
    "real": -2,
    "leer": -3,
    "haz": -4,
    "default": -5,
    "funcion": -6,
    "cadena": -7,
    "escribir": -8,
    "mientras": -9,
    "regresar": -10,
    "vacio": -11,
    "var": -12,
    "si": -13,
    "encaso": -14,
    "ejecutar": -15,
    "entero": -16,
    "sino": -17,
    "caso": -18,
}

arithm_operators = {
    "*": -21,
    "/": -22,
    "%": -23,
    "+": -24,
    "-": -25,
    "=": -26,
}

relat_operators = {
    "<": -31,
    "<=": -32,
    ">": -33,
    ">=": -34,
    "==": -35,
    "!=": -36,
}

log_operators = {
    "!": -41,
    "&&": -42,
    "||": -43,
}

characters = {
    ";": -51,
    "[": -52,
    "]": -53,
    ",": -54,
    ":": -55,
    "(": -56,
    ")": -57,
    "{": -58,
    "}": -59,
}


class Token:
    def __init__(self, lexeme, tkn, pos, line):
        self.lexeme = lexeme
        self.tkn = tkn
        self.pos = pos
        self.line = line


# Expresiones Regulares
typed_id_patt = re.compile("^[a-zA-Z][a-zA-Z0-9]*[&%$@]$")
gral_id_patt = re.compile("^[a-zA-Z][a-zA-Z0-9]*$")

int_const_patt = re.compile("^[+ | -]$")
str_const_patt = re.compile('^".*"$')
comm_patt = re.compile("^//[a-zA-Z0-9]*$")

tokens = []

for i, line in enumerate(lines, start=1):
    words = line.split()
    for word in words:
        if word in res_words:
            tkn = Token(lexeme=word, tkn=res_words.get(word), pos=-1, line=i)
            tokens.append(tkn)
        elif word in arithm_operators:
            tkn = Token(lexeme=word, tkn=arithm_operators.get(word), pos=-1, line=i)
            tokens.append(tkn)
        elif word in relat_operators:
            tkn = Token(lexeme=word, tkn=relat_operators.get(word), pos=-1, line=i)
            tokens.append(tkn)
        elif word in log_operators:
            tkn = Token(lexeme=word, tkn=log_operators.get(word), pos=-1, line=i)
            tokens.append(tkn)
        elif word in characters:
            tkn = Token(lexeme=word, tkn=characters.get(word), pos=-1, line=i)
            tokens.append(tkn)
        elif typed_id_patt.fullmatch(word):
            tkn = Token(lexeme=word, tkn=-91, pos=-2, line=i)
            tokens.append(tkn)
        elif gral_id_patt.fullmatch(word):
            tkn = Token(lexeme=word, tkn=-92, pos=-1, line=i)
            tokens.append(tkn)
        elif str_const_patt.fullmatch(word):
            tkn = Token(lexeme=word, tkn=-95, pos=-1, line=i)
            tokens.append(tkn)
        elif comm_patt.fullmatch(word):
            tkn = Token(lexeme=word, tkn=-96, pos=-1, line=i)
            tokens.append(tkn)
        else:
            try:
                num = int(word)
            except:
                num = float(word)
            if num in range(-32768, 32767):
                tkn = Token(lexeme=word, tkn=-93, pos=-1, line=i)
                tokens.append(tkn)
            else:
                tkn = Token(lexeme=word, tkn=-94, pos=-1, line=i)
                tokens.append(tkn)


token_data = [[token.lexeme, token.tkn, token.pos, token.line] for token in tokens]
headers = ["lexema", "tkn", "pos", "lin"]

print(tabulate(token_data, headers=headers, tablefmt="grid"))
