import re

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
        self.tk = tkn
        self.pos = pos
        self.line = line


tokens = []

for i, line in enumerate(lines, start=1):
    words = line.split()
    for word in words:
        if word in res_words:
            tkn = Token(lexeme=word, tkn=res_words.get(word), pos=-1, line=i)
            tokens.append(tkn)
        if word in arithm_operators:
            tkn = Token(lexeme=word, tkn=arithm_operators.get(word), pos=-1, line=i)
            tokens.append(tkn)
        if word in relat_operators:
            tkn = Token(lexeme=word, tkn=relat_operators.get(word), pos=-1, line=i)
            tokens.append(tkn)
        if word in log_operators:
            tkn = Token(lexeme=word, tkn=log_operators.get(word), pos=-1, line=i)
            tokens.append(tkn)
        if word in characters:
            tkn = Token(lexeme=word, tkn=characters.get(word), pos=-1, line=i)
            tokens.append(tkn)
        if int(word) in range(-32768, 32767):
            int_const_regex = re.compile("^[+ | -]$")
        else:
            real_const_regex = re.compile("^[.]*$")

        int_regex = re.compile("^[a-zA-Z][a-zA-Z0-9]*&$")
        real_regex = re.compile("^[a-zA-Z][a-zA-Z0-9]*%$")
        str_regex = re.compile("^[a-zA-Z][a-zA-Z0-9]*$$")
        cl_meth_regex = re.compile("^[a-zA-Z][a-zA-Z0-9]*@$")

        int_const_regex = re.compile("^[+ | -][]$")
        str_const_regex = re.compile('^"[a-zA-Z0-9]"$')
        comm_regex = re.compile("^//[a-zA-Z0-9]$")
