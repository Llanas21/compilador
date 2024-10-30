from tabulate import tabulate
from models.token_class import TokenClass
from models.sym_table_object import SymTableObject
from models.dir_table_object import DirTableObject


class DuplicatedSymbolError(Exception):
    def __init__(self, symbol_id, scope):
        self.symbol_id = symbol_id
        self.scope = scope
        super().__init__(
            f"Símbolo duplicado encontrado: '{symbol_id}' en el ámbito '{scope}'"
        )


class TypeMismatchError(Exception):
    def __init__(self, variable_id, expected_type, actual_type):
        self.variable_id = variable_id
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
            f"Incompatibilidad de tipo para '{variable_id}': se esperaba {actual_type}, se obtuvo {expected_type}"
        )


class Semantics:
    def __init__(self, file_path):
        self.file_path = file_path
        self.tokens = self.get_tokens()
        self.scope = ""
        self.sym_table_objects = []
        self.dir_table_objects = []

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
                    sym.id == self.tokens[i + 1].lexeme and sym.scope == self.scope
                    for sym in self.sym_table_objects
                ):
                    raise DuplicatedSymbolError(self.tokens[i + 1].lexeme, self.scope)

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

            if self.tokens[i].tkn == "-26":
                actual_type = self.tokens[i - 1].tkn
                expected_type = self.tokens[i + 1].tkn
                if actual_type != expected_type:
                    if actual_type == "-91" and expected_type != "-97":
                        raise TypeMismatchError(
                            variable_id=self.tokens[i - 1].lexeme,
                            expected_type=expected_type,
                            actual_type=actual_type,
                        )
                    elif actual_type == "-92" and expected_type != "-98":
                        raise TypeMismatchError(
                            variable_id=self.tokens[i - 1].lexeme,
                            expected_type=expected_type,
                            actual_type=actual_type,
                        )
                    elif actual_type == "-93" and expected_type != "-95":
                        raise TypeMismatchError(
                            variable_id=self.tokens[i - 1].lexeme,
                            expected_type=expected_type,
                            actual_type=actual_type,
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