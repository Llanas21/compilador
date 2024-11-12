from tabulate import tabulate
from models.token_class import TokenClass, __repr__
from models.op_stack_object import OpStackObject


class IntermediateCode:
    def __init__(self, file_path):
        self.file_path = file_path
        self.tokens = self.get_tokens()
        self.vci = []

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

        self.op_stack = []
        self.dir_stack = []
        self.stat_stack = []

        self.priorities_table = {
            "*": 60,
            "/": 60,
            "%": 60,
            "+": 50,
            "-": 50,
            "<": 40,
            ">": 40,
            "<=": 40,
            ">=": 40,
            "==": 40,
            "!=": 40,
            "NOT": 30,
            "!": 30,
            "AND": 20,
            "&&": 20,
            "OR": 10,
            "||": 10,
            "=": 0,
        }

        self.identifiers = ["-91", "-92", "-93"]

        self.constants = ["-97", "-98", "-96"]

    def get_tokens(self):
        tokens = []
        with open(self.file_path, "r") as file:
            next(file)
            next(file)

            for line in file:
                elements = line.split()
                lexeme = elements[0]
                tkn = elements[1]
                pos = elements[2]
                line = elements[3]
                token = TokenClass(lexeme, tkn, pos, line)
                tokens.append(token)
        return tokens

    def generate_vci(self, output_path):
        for i in range(len(self.tokens)):
            if (
                self.tokens[i].tkn in self.identifiers
                or self.tokens[i].tkn in self.constants
            ):
                self.vci.append(self.tokens[i])
            if (
                self.tokens[i].lexeme in self.arithm_operators
                or self.tokens[i].lexeme in self.relat_operators
                or self.tokens[i].lexeme in self.log_operators
            ):
                op_stack_object = OpStackObject(
                    tkn=self.tokens[i],
                    priority=self.priorities_table.get(self.tokens[i].lexeme),
                )

                while (
                    self.op_stack
                    and op_stack_object.priority <= self.op_stack[-1].priority
                ):
                    self.vci.append(self.op_stack.pop())
                self.op_stack.append(op_stack_object)

            if self.tokens[i].tkn == "-51":
                while self.op_stack:
                    self.vci.append(self.op_stack.pop())

        print(self.vci)
        vci_data = [
            [vci_object.tkn.lexeme, index] for index, vci_object in enumerate(self.vci)
        ]

        vci_headers = ["tkn", "pos"]
        with open(output_path + "vci.txt", "w") as file:
            file.write(tabulate(vci_data, headers=vci_headers, tablefmt="simple"))
