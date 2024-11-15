class DivisionByZero(Exception):
    def __init__(self):

        super().__init__(f"Error, división por cero")


class Execution:
    def __init__(self, file_path):
        self.file_path = file_path
        self.vci = self.get_vci()
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

    def execute(self):
        i = 0
        while i < len(self.vci):
            print(type(self.vci[i]))
            if (
                self.vci[i] in self.arithm_operators
                or self.vci[i] in self.relat_operators
                or self.vci[i] in self.log_operators
            ):
                if self.vci[i] == "*":
                    multiplier = self.exec_stack.pop()
                    multiplicand = self.exec_stack.pop()
                    result = multiplicand * multiplier
                    self.exec_stack.append(result)

                elif self.vci[i] == "/":
                    divisor = self.exec_stack.pop()
                    dividend = self.exec_stack.pop()
                    if divisor != 0:
                        result = dividend / divisor
                    else:
                        raise DivisionByZero()
                    self.exec_stack.append(result)

                elif self.vci[i] == "%":
                    divisor = self.exec_stack.pop()
                    dividend = self.exec_stack.pop()
                    result = dividend % divisor
                    self.exec_stack.append(result)

                elif self.vci[i] == "+":
                    addend1 = self.exec_stack.pop()
                    addend2 = self.exec_stack.pop()
                    result = addend1 + addend2
                    self.exec_stack.append(result)

                elif self.vci[i] == "-":
                    subtrahend = self.exec_stack.pop()
                    minuend = self.exec_stack.pop()
                    result = minuend - subtrahend
                    self.exec_stack.append(result)

                elif self.vci[i] == "=":
                    value = self.exec_stack.pop()
                    identifier = self.exec_stack.pop()
                    print(f"El valor de {identifier} es {value}")
                    #! Actualizar la tabla de símbolos?

                elif self.vci[i] == "<":
                    right = self.exec_stack.pop()
                    left = self.exec_stack.pop()
                    result = 1 if left < right else 0
                    self.exec_stack.append(result)

                elif self.vci[i] == "<=":
                    right = self.exec_stack.pop()
                    left = self.exec_stack.pop()
                    result = 1 if left <= right else 0
                    self.exec_stack.append(result)

                elif self.vci[i] == ">":
                    right = self.exec_stack.pop()
                    left = self.exec_stack.pop()
                    result = 1 if left > right else 0
                    self.exec_stack.append(result)

                elif self.vci[i] == ">=":
                    right = self.exec_stack.pop()
                    left = self.exec_stack.pop()
                    result = 1 if left >= right else 0
                    self.exec_stack.append(result)

                elif self.vci[i] == "==":
                    right = self.exec_stack.pop()
                    left = self.exec_stack.pop()
                    result = 1 if left == right else 0
                    self.exec_stack.append(result)

                elif self.vci[i] == "!=":
                    right = self.exec_stack.pop()
                    left = self.exec_stack.pop()
                    result = 1 if left != right else 0
                    self.exec_stack.append(result)

                elif self.vci[i] == "!":
                    value = self.exec_stack.pop()
                    result = 1 if not value else 0
                    self.exec_stack.append(result)

                elif self.vci[i] == "&&":
                    right = self.exec_stack.pop()
                    left = self.exec_stack.pop()
                    result = 1 if (left and right) else 0
                    self.exec_stack.append(result)

                elif self.vci[i] == "||":
                    right = self.exec_stack.pop()
                    left = self.exec_stack.pop()
                    result = 1 if (left or right) else 0
                    self.exec_stack.append(result)

            else:
                self.exec_stack.append(self.vci[i])

            i += 1
