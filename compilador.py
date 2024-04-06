import re

palabras_reservadas = {
    "programa",
    "real",
    "leer",
    "haz",
    "default",
    "funcion",
    "cadena",
    "escribir",
    "mientras",
    "regresar",
    "vacio",
    "var",
    "si",
    "encaso",
    "ejecutar",
    "entero",
    "sino",
    "caso",
}
operadores_aritmeticos = {"+", "-", "*", "/", "%", "="}
operadores_relacionales = {"<", "<=", ">", ">=", "==", "!="}
operadores_logicos = {"!", "&&", "||"}
token = {";", "[", "]", ",", ":", "(", ")", "{", "}"}
no_token = {'"', ".", " ", "\t"}


# Función para determinar el tipo de identificador
def get_tipo_identificador(token):
    if token.endswith("&"):
        return "entero"
    elif token.endswith("%"):
        return "real"
    elif token.endswith("$"):
        return "cadena"
    elif token.endswith("@"):
        return "programa o función"
    else:
        return "ID"


# Función para procesar el archivo de entrada y generar la tabla de tokens
def generar_tabla_tokens(input_file, output_file):
    with open(input_file, "r") as f:
        data = f.read()

    # Eliminar comentarios
    data = re.sub(r"//.*$", "", data, flags=re.MULTILINE)

    # Tokenizar
    tokens = re.findall(r"\b\w+\b|[^\w\s]", data)

    # Procesar tokens y generar tabla
    table = []
    for token in tokens:
        if token in palabras_reservadas:
            table.append((token, "Palabra Reservada"))
        elif token in operadores_aritmeticos:
            table.append((token, "Operador Aritmético"))
        elif token in operadores_relacionales:
            table.append((token, "Operador Relacional"))
        elif token in operadores_logicos:
            table.append((token, "Operador Lógico"))
        elif token in token:
            table.append((token, "Caracter que genera token"))
        elif token in no_token:
            continue
        elif re.match(r"^[+-]?\d+$", token):  # Constante entera
            table.append((token, "Constante Entera"))
        elif re.match(r"^[+-]?\d+\.\d+$", token):  # Constante real
            table.append((token, "Constante Real"))
        elif token.startswith('"') and token.endswith('"'):  # Constante cadena
            table.append((token, "Constante String"))
        else:
            table.append((token, get_tipo_identificador(token)))

    # Escribir tabla de tokens en el archivo de salida
    with open(output_file, "w") as f:
        f.write("Token\t\tTipo\n")
        for row in table:
            f.write(f"{row[0]}\t\t{row[1]}\n")


# Uso del programa
input_file = "input.txt"
output_file = "output.txt"
generar_tabla_tokens(input_file, output_file)
print("Tabla de tokens generada con éxito en el archivo 'output.txt'.")
