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

    def empty_op_stack(self):
        while self.op_stack:
            self.vci.append(self.op_stack.pop().tkn)

    def generate_empty_tkn(self):
        self.vci.append(TokenClass(lexeme=None, tkn=None, pos=None, line=None))
        self.dir_stack.append(len(self.vci) - 1)

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

    def generate_vci(self, i):

        while i < len(self.tokens):
            print(f"El ciclo de generate_vci se ejecuta {i + 1} veces")

            if (
                self.tokens[i].tkn in self.identifiers
                or self.tokens[i].tkn in self.constants
            ):
                self.vci.append(self.tokens[i])

            elif (
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
                    self.vci.append(self.op_stack.pop().tkn)
                self.op_stack.append(op_stack_object)

            elif self.tokens[i].tkn == "-51":
                self.empty_op_stack()

            elif self.tokens[i].tkn == "-13":
                self.stat_stack.append(self.tokens[i])
                i = self.vci_if(i + 1)
                continue

            elif self.tokens[i].tkn == "-17":
                self.stat_stack.append(self.tokens[i])
                i = self.vci_else(i + 1)
                continue

<<<<<<< HEAD
=======
            elif self.tokens[i].tkn == "-9":
                self.stat_stack.append(self.tokens[i])
                self.dir_stack.append(len(self.vci))
                i = self.vci_while(i + 1)
                continue

            elif self.tokens[i].tkn == "-4":
                self.stat_stack.append(self.tokens[i])
                self.dir_stack.append(len(self.vci))
                i = self.vci_do(i + 1)
                continue

>>>>>>> intermediate_code
            i += 1

        vci_data = [
            [element if isinstance(element, int) else element.lexeme, index]
            for index, element in enumerate(self.vci)
        ]
        vci_headers = ["tkn", "pos"]
        with open(
            r"C:\Users\josel\Universidad\Lenguajes & Autómatas II\compilador\tables\\"
            + "vci.txt",
            "w",
        ) as file:
            file.write(tabulate(vci_data, headers=vci_headers, tablefmt="simple"))

    def vci_if(self, i):
        while i < len(self.tokens):
            print(f"El ciclo de vci_if se ejecuta {i + 1} veces")

            if self.tokens[i].tkn == "-51":
                self.empty_op_stack()
            elif (
                self.tokens[i].tkn in self.identifiers
                or self.tokens[i].tkn in self.constants
            ):
                self.vci.append(self.tokens[i])
            elif (
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
                    self.vci.append(self.op_stack.pop().tkn)
                self.op_stack.append(op_stack_object)

            elif self.tokens[i].tkn == "-57":
                self.empty_op_stack()
                self.generate_empty_tkn()
                self.vci.append(
                    TokenClass(
                        lexeme="si",
                        tkn="-13",
                        pos="-1",
                        line=self.tokens[i].line,
                    )
                )

            elif self.tokens[i].tkn == "-59":
                element = self.stat_stack.pop()
                if element.lexeme == "si":
                    return i + 1

            i += 1

    def vci_else(self, i):
        dir_value = self.dir_stack.pop()
        self.vci[dir_value] = len(self.vci) + 2
        self.generate_empty_tkn()
        self.vci.append(
            TokenClass(
                lexeme="sino",
                tkn="-17",
                pos="-1",
                line=self.tokens[i].line,
            )
        )

        while i < len(self.tokens):
            print(f"El ciclo de vci_else se ejecuta {i + 1} veces")

            if self.tokens[i].tkn == "-51":
                self.empty_op_stack()
            elif (
                self.tokens[i].tkn in self.identifiers
                or self.tokens[i].tkn in self.constants
            ):
                self.vci.append(self.tokens[i])
            elif (
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
                    self.vci.append(self.op_stack.pop().tkn)
                self.op_stack.append(op_stack_object)

            elif self.tokens[i].tkn == "-59":
                element = self.stat_stack.pop()
                if element.lexeme == "sino":
                    dir_value = self.dir_stack.pop()
                    self.vci[dir_value] = len(self.vci)
                    return i + 1

            i += 1
<<<<<<< HEAD
=======

    def vci_while(self, i):
        while i < len(self.tokens):
            if self.tokens[i].tkn == "-51":
                self.empty_op_stack()
            elif (
                self.tokens[i].tkn in self.identifiers
                or self.tokens[i].tkn in self.constants
            ):
                self.vci.append(self.tokens[i])
            elif (
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
                    self.vci.append(self.op_stack.pop().tkn)
                self.op_stack.append(op_stack_object)

            elif self.tokens[i].tkn == "-57":
                self.empty_op_stack()
                self.generate_empty_tkn()
                self.vci.append(
                    TokenClass(
                        lexeme="mientras",
                        tkn="-9",
                        pos="-1",
                        line=self.tokens[i].line,
                    )
                )

            elif self.tokens[i].tkn == "-59":
                element = self.stat_stack.pop()
                if element.lexeme == "mientras":
                    dir_value = self.dir_stack.pop()
                    self.vci[dir_value] = len(self.vci) + 2
                    dir_value = self.dir_stack.pop()
                    self.vci.append(dir_value)
                    self.vci.append(
                        TokenClass(
                            lexeme="endW",
                            tkn=None,
                            pos=None,
                            line=None,
                        )
                    )
                    return i + 1

            i += 1

    def vci_do(self, i):
        while i < len(self.tokens):
            if self.tokens[i].tkn == "-51":
                self.empty_op_stack()
            elif (
                self.tokens[i].tkn in self.identifiers
                or self.tokens[i].tkn in self.constants
            ):
                self.vci.append(self.tokens[i])
            elif (
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
                    self.vci.append(self.op_stack.pop().tkn)
                self.op_stack.append(op_stack_object)

            elif self.tokens[i].tkn == "-59":
                element = self.stat_stack.pop()
                if element.lexeme == "haz":
                    pass

            elif self.tokens[i].tkn == "-57":
                self.empty_op_stack()
                dir_value = self.dir_stack.pop()
                self.vci.append(dir_value)
                self.vci.append(
                    TokenClass(
                        lexeme="finDo",
                        tkn=None,
                        pos=None,
                        line=None,
                    )
                )
                return i + 1

            i += 1
>>>>>>> intermediate_code
