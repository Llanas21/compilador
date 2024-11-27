import re
from tabulate import tabulate
from models.sym_table_object import SymTableObject
import tkinter as tk
from tkinter import messagebox


class DivisionByZero(Exception):
    def __init__(self):

        super().__init__(f"Error, división por cero")


class Execution:
    def __init__(self, file_path):
        self.file_path = file_path
        self.vci = self.get_vci()
        self.sym_table_objects = self.get_symbols_table()
        self.exec_stack = []

        self.arithm_operators = [
            "*",
            "/",
            "%",
            "+",
            "-",
            "=",
        ]

        self.relat_operators = [
            "<",
            "<=",
            ">",
            ">=",
            "==",
            "!=",
        ]

        self.log_operators = [
            "!",
            "&&",
            "||",
        ]

        self.statutes = [
            "si",
            "sino",
            "mientras",
            "haz",
            "finW",
            "finDo",
        ]

        self.methods = [
            "leer",
            "escribir",
        ]

        self.identifiers = ["-91", "-92", "-93"]

        self.int_id_patt = re.compile("^[a-zA-Z][a-zA-Z0-9]*&$")
        self.real_id_patt = re.compile("^[a-zA-Z][a-zA-Z0-9]*%$")
        self.str_id_patt = re.compile(r"^[a-zA-Z][a-zA-Z0-9]*\$$")

    def is_identifier(self, tkn):
        if isinstance(tkn, str):
            if (
                self.int_id_patt.fullmatch(tkn)
                or self.real_id_patt.fullmatch(tkn)
                or self.str_id_patt.fullmatch(tkn)
            ):
                return True

            else:
                return False
        else:
            return False

    def get_id_value(self, id):
        index = next(
            (
                index
                for index, sym_table_object in enumerate(self.sym_table_objects)
                if sym_table_object.id == id
            ),
            -1,
        )
        # try:
        #     value = int(self.sym_table_objects[index].value)
        # except:
        #     value = float(self.sym_table_objects[index].value)

        if self.int_id_patt.fullmatch(id):
            return int(self.sym_table_objects[index].value)
        elif self.real_id_patt.fullmatch(id):
            return float(self.sym_table_objects[index].value)

    def get_vci(self):
        vci = []

        with open(self.file_path, "r") as file:
            next(file)
            next(file)

            for line in file:
                elements = line.split()
                try:
                    value = int(elements[0])
                    vci.append(value)
                except ValueError:
                    try:
                        value = float(elements[0])
                        vci.append(value)
                    except ValueError:
                        vci.append(elements[0])

        return vci

    def get_symbols_table(self):
        sym_table_objects = []

        with open(
            r"C:\Users\josel\Universidad\Lenguajes & Autómatas II\compilador\tables\symbols_table.txt",
            "r",
        ) as file:
            next(file)
            next(file)

            for line in file:
                elements = line.split()
                id = elements[0]
                tkn = elements[1]
                value = elements[2]
                d2 = elements[3]
                d1 = elements[4]
                ptr = elements[5]
                scope = elements[6]
                sym_table_object = SymTableObject(
                    id,
                    tkn,
                    value,
                    d2,
                    d1,
                    ptr,
                    scope,
                )
                sym_table_objects.append(sym_table_object)

        return sym_table_objects

    def execute(self):
        i = 0
        while i < len(self.vci):

            if (
                self.vci[i] in self.arithm_operators
                or self.vci[i] in self.relat_operators
                or self.vci[i] in self.log_operators
                or self.vci[i] in self.statutes
                or self.vci[i] in self.methods
            ):
                if self.vci[i] == "*":

                    multiplier = self.exec_stack.pop()
                    if self.is_identifier(multiplier):
                        multiplier = self.get_id_value(multiplier)
                    multiplicand = self.exec_stack.pop()
                    if self.is_identifier(multiplicand):
                        multiplicand = self.get_id_value(multiplicand)

                    result = multiplicand * multiplier
                    self.exec_stack.append(result)

                elif self.vci[i] == "/":

                    divisor = self.exec_stack.pop()
                    if self.is_identifier(divisor):
                        divisor = self.get_id_value(divisor)
                    dividend = self.exec_stack.pop()
                    if self.is_identifier(dividend):
                        dividend = self.get_id_value(dividend)
                    if divisor != 0:
                        result = dividend / divisor
                    else:
                        raise DivisionByZero()
                    self.exec_stack.append(result)

                elif self.vci[i] == "%":

                    divisor = self.exec_stack.pop()
                    if self.is_identifier(divisor):
                        divisor = self.get_id_value(divisor)
                    dividend = self.exec_stack.pop()
                    if self.is_identifier(dividend):
                        dividend = self.get_id_value(dividend)
                    result = dividend % divisor
                    self.exec_stack.append(result)

                elif self.vci[i] == "+":

                    addend1 = self.exec_stack.pop()
                    if self.is_identifier(addend1):
                        addend1 = self.get_id_value(addend1)
                    addend2 = self.exec_stack.pop()
                    if self.is_identifier(addend2):
                        addend2 = self.get_id_value(addend2)
                    result = addend1 + addend2
                    self.exec_stack.append(result)

                elif self.vci[i] == "-":

                    subtrahend = self.exec_stack.pop()
                    if self.is_identifier(subtrahend):
                        subtrahend = self.get_id_value(subtrahend)
                    minuend = self.exec_stack.pop()
                    if self.is_identifier(minuend):
                        minuend = self.get_id_value(minuend)
                    result = minuend - subtrahend
                    self.exec_stack.append(result)

                elif self.vci[i] == "=":
                    value = self.exec_stack.pop()
                    if self.is_identifier(value):
                        value = self.get_id_value(value)
                    identifier = self.exec_stack.pop()
                    index = next(
                        (
                            index
                            for index, sym_table_object in enumerate(
                                self.sym_table_objects
                            )
                            if sym_table_object.id == identifier
                        ),
                        -1,
                    )

                    self.sym_table_objects[index].value = value

                if self.vci[i] == "<":
                    right = self.exec_stack.pop()

                    if self.is_identifier(right):
                        right = self.get_id_value(right)
                    left = self.exec_stack.pop()

                    if self.is_identifier(left):

                        left = self.get_id_value(left)

                    result = 1 if left < right else 0
                    self.exec_stack.append(result)

                elif self.vci[i] == "<=":

                    right = self.exec_stack.pop()
                    if self.is_identifier(right):
                        right = self.get_id_value(right)
                    left = self.exec_stack.pop()
                    if self.is_identifier(left):
                        left = self.get_id_value(left)
                    result = 1 if left <= right else 0
                    self.exec_stack.append(result)

                elif self.vci[i] == ">":

                    right = self.exec_stack.pop()
                    if self.is_identifier(right):
                        right = self.get_id_value(right)
                    left = self.exec_stack.pop()
                    if self.is_identifier(left):
                        left = self.get_id_value(left)
                    result = 1 if left > right else 0
                    self.exec_stack.append(result)

                elif self.vci[i] == ">=":

                    right = self.exec_stack.pop()
                    if self.is_identifier(right):
                        right = self.get_id_value(right)
                    left = self.exec_stack.pop()
                    if self.is_identifier(left):
                        left = self.get_id_value(left)
                    result = 1 if left >= right else 0
                    self.exec_stack.append(result)

                elif self.vci[i] == "==":

                    right = self.exec_stack.pop()
                    if self.is_identifier(right):
                        right = self.get_id_value(right)
                    left = self.exec_stack.pop()
                    if self.is_identifier(left):
                        left = self.get_id_value(left)
                    result = 1 if left == right else 0
                    self.exec_stack.append(result)

                elif self.vci[i] == "!=":

                    right = self.exec_stack.pop()
                    if self.is_identifier(right):
                        right = self.get_id_value(right)
                    left = self.exec_stack.pop()
                    if self.is_identifier(left):
                        left = self.get_id_value(left)
                    result = 1 if left != right else 0
                    self.exec_stack.append(result)

                elif self.vci[i] == "!":
                    value = self.exec_stack.pop()
                    if self.is_identifier(value):
                        value = self.get_id_value(value)
                    result = 1 if not value else 0
                    self.exec_stack.append(result)

                elif self.vci[i] == "&&":

                    right = self.exec_stack.pop()
                    if self.is_identifier(right):
                        right = self.get_id_value(right)
                    left = self.exec_stack.pop()
                    if self.is_identifier(left):
                        left = self.get_id_value(left)
                    result = 1 if (left and right) else 0
                    self.exec_stack.append(result)

                elif self.vci[i] == "||":

                    right = self.exec_stack.pop()
                    if self.is_identifier(right):
                        right = self.get_id_value(right)
                    left = self.exec_stack.pop()
                    if self.is_identifier(left):
                        left = self.get_id_value(left)
                    result = 1 if (left or right) else 0
                    self.exec_stack.append(result)

                elif self.vci[i] == "leer":

                    identifier = self.exec_stack.pop()
                    value = input(f"Ingresa el valor para {identifier}: ")

                    index = next(
                        (
                            index
                            for index, sym_table_object in enumerate(
                                self.sym_table_objects
                            )
                            if sym_table_object.id == identifier
                        ),
                        -1,
                    )

                    self.sym_table_objects[index].value = value

                elif self.vci[i] == "escribir":

                    param = self.exec_stack.pop()

                    if self.is_identifier(param):
                        value = self.get_id_value(param)
                        print(value)
                    else:
                        print(param)

                elif self.vci[i] == "si":
                    dir_value = self.exec_stack.pop()
                    truth_value = self.exec_stack.pop()
                    if truth_value == 1:
                        i += 1
                        continue
                    else:
                        i = dir_value
                        continue

                elif self.vci[i] == "sino":
                    dir_value = self.exec_stack.pop()
                    i = dir_value

                elif self.vci[i] == "mientras":
                    dir_value = self.exec_stack.pop()
                    truth_value = self.exec_stack.pop()
                    if truth_value == 1:
                        i += 1
                        continue
                    else:
                        i = dir_value
                        continue

                elif self.vci[i] == "finW":
                    dir_value = self.exec_stack.pop()
                    i = dir_value
                    continue

                elif self.vci[i] == "finDo":
                    dir_value = self.exec_stack.pop()
                    truth_value = self.exec_stack.pop()
                    if truth_value == 1:
                        i = dir_value
                        continue
                    else:
                        i += 1
                        continue

            else:
                self.exec_stack.append(self.vci[i])

            i += 1

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
        with open(
            r"C:\Users\josel\Universidad\Lenguajes & Autómatas II\compilador\tables\\"
            + "symbols_table.txt",
            "w",
        ) as file:
            file.write(
                tabulate(symbol_data, headers=symbols_table_headers, tablefmt="simple")
            )
