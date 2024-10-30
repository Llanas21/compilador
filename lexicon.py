import re
from tabulate import tabulate
from models.token_class import TokenClass


class InvalidIdentifierError(Exception):
    def __init__(self, word):
        self.word = word
        super().__init__(f"Identificador no válido: {word}")


class Lexicon:
    def __init__(self, file_path):
        self.file_path = file_path
        self.res_words = {
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

        self.arithm_operators = {
            "*": -21,
            "/": -22,
            "%": -23,
            "+": -24,
            "-": -25,
            "=": -26,
        }

        self.relat_operators = {
            "<": -31,
            "<=": -32,
            ">": -33,
            ">=": -34,
            "==": -35,
            "!=": -36,
        }

        self.log_operators = {
            "!": -41,
            "&&": -42,
            "||": -43,
        }

        self.characters = {
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

        self.non_tkn = [
            '"',
            ".",
            " ",
            "\t",
            "\n",
        ]

        self.int_id_patt = re.compile("^[a-zA-Z][a-zA-Z0-9]*&$")
        self.real_id_patt = re.compile("^[a-zA-Z][a-zA-Z0-9]*%$")
        self.str_id_patt = re.compile(r"^[a-zA-Z][a-zA-Z0-9]*\$$")
        self.cl_meth_id_patt = re.compile("^[a-zA-Z][a-zA-Z0-9]*@$")
        self.str_const_patt = re.compile('^".*"$')
        self.comm_patt = re.compile("^//[a-zA-Z0-9]*$")

        self.tokens = []

    def generateTokensTable(self, output_path):
        with open(self.file_path, "r") as file:
            lines = file.read().splitlines()

        for i, line in enumerate(lines, start=1):
            words = line.split()
            for word in words:
                if word in self.res_words:
                    tkn = TokenClass(
                        lexeme=word, tkn=self.res_words.get(word), pos=-1, line=i
                    )
                    self.tokens.append(tkn)
                elif word in self.arithm_operators:
                    tkn = TokenClass(
                        lexeme=word, tkn=self.arithm_operators.get(word), pos=-1, line=i
                    )
                    self.tokens.append(tkn)
                elif word in self.relat_operators:
                    tkn = TokenClass(
                        lexeme=word, tkn=self.relat_operators.get(word), pos=-1, line=i
                    )
                    self.tokens.append(tkn)
                elif word in self.log_operators:
                    tkn = TokenClass(
                        lexeme=word, tkn=self.log_operators.get(word), pos=-1, line=i
                    )
                    self.tokens.append(tkn)
                elif word in self.characters:
                    tkn = TokenClass(
                        lexeme=word, tkn=self.characters.get(word), pos=-1, line=i
                    )
                    self.tokens.append(tkn)
                elif self.int_id_patt.fullmatch(word):
                    tkn = TokenClass(lexeme=word, tkn=-91, pos=-2, line=i)
                    self.tokens.append(tkn)
                elif self.real_id_patt.fullmatch(word):
                    tkn = TokenClass(lexeme=word, tkn=-92, pos=-2, line=i)
                    self.tokens.append(tkn)
                elif self.str_id_patt.fullmatch(word):
                    tkn = TokenClass(lexeme=word, tkn=-93, pos=-2, line=i)
                    self.tokens.append(tkn)
                elif self.cl_meth_id_patt.fullmatch(word):
                    tkn = TokenClass(lexeme=word, tkn=-94, pos=-2, line=i)
                    self.tokens.append(tkn)
                elif self.str_const_patt.fullmatch(word):
                    tkn = TokenClass(lexeme=word, tkn=-95, pos=-1, line=i)
                    self.tokens.append(tkn)
                elif self.comm_patt.fullmatch(word):
                    tkn = TokenClass(lexeme=word, tkn=-96, pos=-1, line=i)
                    self.tokens.append(tkn)
                elif word in self.non_tkn:
                    pass
                else:
                    try:
                        num = int(word)
                        tkn = TokenClass(lexeme=word, tkn=-97, pos=-1, line=i)
                        self.tokens.append(tkn)
                    except ValueError:
                        try:
                            num = float(word)
                            tkn = TokenClass(lexeme=word, tkn=-98, pos=-1, line=i)
                            self.tokens.append(tkn)
                        except ValueError:
                            raise InvalidIdentifierError(word=word)

        token_data = [
            [token.lexeme, token.tkn, token.pos, token.line] for token in self.tokens
        ]
        headers = ["lexema", "tkn", "pos", "lin"]

        file = open(output_path, "w")
        file.write(tabulate(token_data, headers=headers, tablefmt="simple"))
