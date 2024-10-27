from tabulate import tabulate
from token_class import TokenClass
from sym_table_object import SymTableObject
from dir_table_object import DirTableObject


def get_tokens(file_path):
    tokens = []
    with open(file_path, "r") as file:
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


tokens = get_tokens("tables/tokens_table.txt")

scope = ""
sym_table_objects = []
dir_table_objects = []

for i in range(len(tokens)):

    if tokens[i].tkn == "-1":
        dir_table_object = DirTableObject(
            id=tokens[i + 1].lexeme,
            tkn=tokens[i + 1].tkn,
            line=tokens[i + 1].line,
            vci=0,
        )
        scope = dir_table_object.id
        dir_table_objects.append(dir_table_object)
        print(dir_table_object.id)

    if tokens[i].tkn == "-12":
        sym_table_object = SymTableObject(
            id=tokens[i + 1].lexeme,
            tkn=tokens[i + 1].tkn,
            value=0,
            d1=0,
            d2=0,
            ptr=None,
            scope=scope,
        )
        sym_table_objects.append(sym_table_object)

        print(sym_table_object.id)

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
    for sym_table_object in sym_table_objects
]

symbols_table_headers = ["id", "tkn", "value", "d2", "d1", "ptr", "scope"]

direction_data = [
    [
        dir_table_object.id,
        dir_table_object.tkn,
        dir_table_object.line,
        dir_table_object.vci,
    ]
    for dir_table_object in dir_table_objects
]

directions_table_headers = ["id", "tkn", "line", "vci"]


def generateSymbolsTable():
    file = open("tables/symbols_table.txt", "w")
    file.write(tabulate(symbol_data, headers=symbols_table_headers, tablefmt="simple"))


def generateDirectionsTable():
    file = open("tables/directions_table.txt", "w")
    file.write(
        tabulate(direction_data, headers=directions_table_headers, tablefmt="simple")
    )
