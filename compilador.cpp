#include <iostream>
#include <string>
#include <vector>
#include <sstream>

using namespace std;

// Estructura para representar un token
struct Token
{
    string lexema;
    int id;
    int tipo; // -1 para no identificador, -2 para identificador
    int linea;
};

// Función para desglosar una línea en tokens
vector<Token> desglosarLinea(const string &linea, int numLinea)
{
    vector<Token> tokens;
    stringstream ss(linea);
    string token;

    while (ss >> token)
    {
        Token tkn;
        tkn.lexema = token;

        // Ignorar comentarios
        if (token.find("//") == 0)
        {
            break; // Salir del bucle al encontrar un comentario
        }

        // Asignación de token y tipo
        if (token == "programa")
        {
            tkn.id = -1;
            tkn.tipo = -1;
        }
        else if (token == "funcion")
        {
            tkn.id = -2;
            tkn.tipo = -1;
        }
        else if (token == "vacio")
        {
            tkn.id = -3;
            tkn.tipo = -1;
        }
        else if (token == "entero")
        {
            tkn.id = -4;
            tkn.tipo = -51;
        }
        else if (token == "real")
        {
            tkn.id = -5;
            tkn.tipo = -52;
        }
        else if (token == "cadena")
        {
            tkn.id = -6;
            tkn.tipo = -53;
        }
        else if (token == "var")
        {
            tkn.id = -7;
            tkn.tipo = -1;
        }
        else if (token == "leer")
        {
            tkn.id = -8;
            tkn.tipo = -1;
        }
        else if (token == "escribir")
        {
            tkn.id = -9;
            tkn.tipo = -1;
        }
        else if (token == "si")
        {
            tkn.id = -10;
            tkn.tipo = -1;
        }
        else if (token == "sino")
        {
            tkn.id = -11;
            tkn.tipo = -1;
        }
        else if (token == "haz")
        {
            tkn.id = -12;
            tkn.tipo = -1;
        }
        else if (token == "mientras")
        {
            tkn.id = -13;
            tkn.tipo = -1;
        }
        else if (token == "encaso")
        {
            tkn.id = -14;
            tkn.tipo = -1;
        }
        else if (token == "caso")
        {
            tkn.id = -15;
            tkn.tipo = -1;
        }
        else if (token == "default")
        {
            tkn.id = -16;
            tkn.tipo = -1;
        }
        else if (token == "regresar")
        {
            tkn.id = -17;
            tkn.tipo = -1;
        }
        else if (token == "ejecutar")
        {
            tkn.id = -18;
            tkn.tipo = -1;
        }
        else if (token == "*")
        {
            tkn.id = -21;
            tkn.tipo = -1;
        }
        else if (token == "/")
        {
            tkn.id = -22;
            tkn.tipo = -1;
        }
        else if (token == "%")
        {
            tkn.id = -23;
            tkn.tipo = -1;
        }
        else if (token == "+")
        {
            tkn.id = -24;
            tkn.tipo = -1;
        }
        else if (token == "-")
        {
            tkn.id = -25;
            tkn.tipo = -1;
        }
        else if (token == "=")
        {
            tkn.id = -26;
            tkn.tipo = -1;
        }
        else if (token == "<")
        {
            tkn.id = -31;
            tkn.tipo = -1;
        }
        else if (token == "<=")
        {
            tkn.id = -32;
            tkn.tipo = -1;
        }
        else if (token == ">")
        {
            tkn.id = -33;
            tkn.tipo = -1;
        }
        else if (token == ">=")
        {
            tkn.id = -34;
            tkn.tipo = -1;
        }
        else if (token == "==")
        {
            tkn.id = -35;
            tkn.tipo = -1;
        }
        else if (token == "!=")
        {
            tkn.id = -36;
            tkn.tipo = -1;
        }
        else if (token == "&&")
        {
            tkn.id = -41;
            tkn.tipo = -1;
        }
        else if (token == "||")
        {
            tkn.id = -42;
            tkn.tipo = -1;
        }
        else if (token == "!")
        {
            tkn.id = -43;
            tkn.tipo = -1;
        }
        else if (token == "[")
        {
            tkn.id = -71;
            tkn.tipo = -1;
        }
        else if (token == "]")
        {
            tkn.id = -72;
            tkn.tipo = -1;
        }
        else if (token == "(")
        {
            tkn.id = -73;
            tkn.tipo = -1;
        }
        else if (token == ")")
        {
            tkn.id = -74;
            tkn.tipo = -1;
        }
        else if (token == ";")
        {
            tkn.id = -75;
            tkn.tipo = -1;
        }
        else if (token == ",")
        {
            tkn.id = -76;
            tkn.tipo = -1;
        }
        else if (isdigit(token[0]))
        {
            // Verificar si es un número real
            bool esReal = false;
            for (char c : token)
            {
                if (c == '.')
                {
                    esReal = true;
                    break;
                }
            }

            // Asignar el token apropiado
            if (esReal)
            {
                tkn.id = -62;
            }
            else
            {
                // Constante entera
                try
                {
                    int valor = stoi(token);
                    if (valor >= -32768 && valor <= 32767)
                    {
                        tkn.id = -61;
                    }
                    else
                    {
                        throw out_of_range("");
                    }
                }
                catch (const out_of_range &e)
                {
                    // Si el valor está fuera del rango de los enteros, considerarlo real
                    tkn.id = -62;
                }
            }
            tkn.tipo = -1; // Tipo de constante
        }
        else if (token.size() >= 2 && token[0] == '"' && token[token.size() - 1] == '"')
        {
            // Constante cadena
            tkn.id = -63;
            tkn.tipo = -1;
        }
        else
        {
            // Si el token no coincide con ninguno de los anteriores, asumimos que es un identificador
            tkn.id = -54;
            tkn.tipo = -2;
        }

        // Obtener número de línea
        tkn.linea = numLinea;

        tokens.push_back(tkn);
    }

    return tokens;
}

int main()
{

    string linea;
    vector<vector<Token>> desgloses;
    int numLinea = 1;

    // Leer líneas hasta que se ingrese una línea vacía o un comentario
    while ((getline(cin, linea)) && (linea != "//comentario") && (!linea.empty()))
    {
        // Desglosar la línea en tokens
        vector<Token> tokens = desglosarLinea(linea, numLinea);
        desgloses.push_back(tokens);
        numLinea++;
    }

    // Imprimir los desgloses
    for (size_t i = 0; i < desgloses.size(); ++i)
    {
        for (size_t j = 0; j < desgloses[i].size(); ++j)
        {
            const Token &token = desgloses[i][j];
            cout << token.lexema << " " << token.id << " " << token.tipo << " " << token.linea << endl;
        }
    }

    return 0;
}