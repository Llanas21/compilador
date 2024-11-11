from tabulate import tabulate
from models.token_class import TokenClass
from models.sym_table_object import SymTableObject
from models.dir_table_object import DirTableObject


class UndeclaredSymbolError(Exception):
    def __init__(self, tkn, scope):
        self.tkn = tkn
        self.scope = scope
        super().__init__(
            f"Error en la línea {tkn.line}\nSímbolo no inicializado encontrado: '{tkn.lexeme}' en el ámbito '{scope}'"
        )


class DuplicatedSymbolError(Exception):
    def __init__(self, tkn, scope):
        self.tkn = tkn
        self.scope = scope
        super().__init__(
            f"Error en la línea {tkn.line}\nSímbolo duplicado encontrado: '{tkn.lexeme}' en el ámbito '{scope}'"
        )


class TypeMismatchError(Exception):
    def __init__(self, tkn, expected_type, actual_type):
        self.tkn = tkn
        self.expected_type = expected_type
        self.actual_type = actual_type

        if expected_type == "-91" or expected_type == "-97":
            expected_type = "entero"
        elif expected_type == "-92" or expected_type == "-98":
            expected_type = "flotante"
        elif expected_type == "-93" or expected_type == "-95":
            expected_type = "cadena"
        else:
            pass

        if actual_type == "-91" or actual_type == "-97":
            actual_type = "entero"
        elif actual_type == "-92" or actual_type == "-98":
            actual_type = "flotante"
        elif actual_type == "-93" or actual_type == "-95":
            actual_type = "cadena"
        else:
            pass

        super().__init__(
            f"Error en la línea {tkn.line}\nIncompatibilidad de tipo para '{tkn.lexeme}': se esperaba {expected_type}, se obtuvo {actual_type}"
        )


class Semantics:
    def __init__(self, file_path):
        self.file_path = file_path
        self.tokens = self.get_tokens()
        self.scope = ""
        self.sym_table_objects = []
        self.dir_table_objects = []

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

    def generate_dir_sym_tables(self, output_path):
        for i in range(len(self.tokens)):
            if self.tokens[i].tkn == "-1":
                dir_table_object = DirTableObject(
                    id=self.tokens[i + 1].lexeme,
                    tkn=self.tokens[i + 1].tkn,
                    line=self.tokens[i + 1].line,
                    vci=0,
                )
                self.scope = dir_table_object.id
                self.dir_table_objects.append(dir_table_object)

            if self.tokens[i].tkn == "-12":
                if any(
                    sym_table_object.id == self.tokens[i + 1].lexeme
                    and sym_table_object.scope == self.scope
                    for sym_table_object in self.sym_table_objects
                ):
                    raise DuplicatedSymbolError(self.tokens[i + 1], self.scope)

                sym_table_object = SymTableObject(
                    id=self.tokens[i + 1].lexeme,
                    tkn=self.tokens[i + 1].tkn,
                    value=0,
                    d1=0,
                    d2=0,
                    ptr=None,
                    scope=self.scope,
                )
                self.sym_table_objects.append(sym_table_object)

            if self.tokens[i].tkn == "-54":
                if any(
                    sym_table_object.id == self.tokens[i + 1].lexeme
                    and sym_table_object.scope == self.scope
                    for sym_table_object in self.sym_table_objects
                ):
                    raise DuplicatedSymbolError(self.tokens[i + 1], self.scope)

                sym_table_object = SymTableObject(
                    id=self.tokens[i + 1].lexeme,
                    tkn=self.tokens[i + 1].tkn,
                    value=0,
                    d1=0,
                    d2=0,
                    ptr=None,
                    scope=self.scope,
                )
                self.sym_table_objects.append(sym_table_object)

            if (
                self.tokens[i].lexeme in self.arithm_operators
                or self.tokens[i].lexeme in self.relat_operators
            ):

                if not any(
                    self.tokens[i - 1].lexeme == sym_table_object.id
                    and sym_table_object.scope == self.scope
                    for sym_table_object in self.sym_table_objects
                ):
                    if self.tokens[i - 1].tkn not in [
                        "-95",
                        "-97",
                        "-98",
                        "-56",
                        "-57",
                    ]:
                        raise UndeclaredSymbolError(
                            tkn=self.tokens[i - 1], scope=self.scope
                        )
                    else:
                        pass

            if (
                self.tokens[i].tkn in self.identifiers
                or self.tokens[i].tkn in self.constants
            ):
                inline_tokens = [
                    token
                    for token in self.tokens
                    if token.line == self.tokens[i].line
                    and (token.tkn in self.identifiers or token.tkn in self.constants)
                ]

                if self.tokens[i].tkn == "-91" or self.tokens[i].tkn == "-97":
                    mismatched_token = next(
                        (
                            token
                            for token in inline_tokens
                            if token.tkn != "-91" and token.tkn != "-97"
                        ),
                        None,
                    )

                    if mismatched_token is not None:
                        raise TypeMismatchError(
                            tkn=self.tokens[i],
                            expected_type="-91",
                            actual_type=mismatched_token.tkn,
                        )

                if self.tokens[i].tkn == "-92" or self.tokens[i].tkn == "-98":
                    mismatched_token = next(
                        (
                            token
                            for token in inline_tokens
                            if token.tkn != "-92" and token.tkn != "-98"
                        ),
                        None,
                    )

                    if mismatched_token is not None:
                        raise TypeMismatchError(
                            tkn=self.tokens[i],
                            expected_type="-92",
                            actual_type=mismatched_token.tkn,
                        )

                if self.tokens[i].tkn == "-93" or self.tokens[i].tkn == "-96":
                    mismatched_token = next(
                        (
                            token
                            for token in inline_tokens
                            if token.tkn != "-93" and token.tkn != "-96"
                        ),
                        None,
                    )

                    if mismatched_token is not None:
                        raise TypeMismatchError(
                            tkn=self.tokens[i],
                            expected_type="-93",
                            actual_type=mismatched_token.tkn,
                        )

        symbol_data = [
            [
                sym_table_object.id,
                sym_table_object.tkn,
                sym_table_object.value,
                sym_table_object.d2,
                sym_table_object.d1,
                sym_table_object.ptr,
                sym_table_object.scope,
            ]
            for sym_table_object in self.sym_table_objects
        ]

        symbols_table_headers = ["id", "tkn", "value", "d2", "d1", "ptr", "scope"]
        with open(output_path + "symbols_table.txt", "w") as file:
            file.write(
                tabulate(symbol_data, headers=symbols_table_headers, tablefmt="simple")
            )

        direction_data = [
            [
                dir_table_object.id,
                dir_table_object.tkn,
                dir_table_object.line,
                dir_table_object.vci,
            ]
            for dir_table_object in self.dir_table_objects
        ]

        directions_table_headers = ["id", "tkn", "line", "vci"]
        with open(output_path + "directions_table.txt", "w") as file:
            file.write(
                tabulate(
                    direction_data, headers=directions_table_headers, tablefmt="simple"
                )
            )
