import hashlib
import time
import re


def imprimir_resultados(contador, ceros, sha256, valor_hex):
    print("===TIEMPO LIMITE (240s) ALCANZADO===")
    print(f"Iteraciones calculadas: {contador}")
    print(f"Hash con {ceros} ceros encontrado: {sha256}")
    print(f"Valor HEX con el que se ha obtenido: {valor_hex}")


def contar_ceros_iniciales(cadena):
    # Encuentra una o más ocurrencias de '0' al comienzo de la cadena
    match = re.match(r'^0+', cadena)
    if match:
        return len(match.group(0))  # Cantidad de ceros iniciales
    else:
        return 0


def calcular_sha256(datos):
    sha256 = hashlib.sha256()
    sha256.update(datos)
    return sha256.hexdigest()


def encontrar_hex_sha256(nombre_fichero_entrada, nombre_fichero_salida):
    # Leer el contenido del fichero de entrada
    with open(nombre_fichero_entrada, "rb") as archivo:
        datos = archivo.read()

    valor_hex = "00000000"  # Generar un valor hexadecimal inicial
    timeout = time.time() + 240  # Dentro de 240 segundos

    sha256_max_ceros = ""
    max_ceros = 0
    valor_hex_max_ceros = valor_hex

    contador = 0
    while True:
        if time.time() > timeout:
            # Escribir el valor hash con el que más ceros se obtiene
            with open(nombre_fichero_salida, "wb") as salida:
                salida.write(datos)
                salida.write(f"\n{valor_hex_max_ceros}\tbad\t100".encode("utf-8"))
            imprimir_resultados(contador, max_ceros, sha256_max_ceros, valor_hex_max_ceros)
            break

        datos_con_linea = datos + f"\n{valor_hex}\tbad\t100".encode("utf-8")

        sha256 = calcular_sha256(datos_con_linea)

        cantidad_ceros = contar_ceros_iniciales(sha256)
        # print(f"(Ceros,Hex,SHA-256) = ({cantidad_ceros}, {valor_hex}, {sha256})")
        if cantidad_ceros > max_ceros:
            max_ceros = cantidad_ceros
            sha256_max_ceros = sha256
            valor_hex_max_ceros = valor_hex
            print(f"MAX: (Ceros,Hex,SHA-256) = ({cantidad_ceros}, {valor_hex}, {sha256})")

        valor_hex = format(int(valor_hex, 16) + contador, "08x")
        datos_con_linea = datos + f"\n{valor_hex}\tbad\t100".encode("utf-8")
        contador += 1


def crear_fichero_salida(nombre_fichero_entrada, nombre_fichero_salida):
    encontrar_hex_sha256(nombre_fichero_entrada, nombre_fichero_salida)
    print("Fichero de salida creado con éxito.")


if __name__ == "__main__":
    # nombre_archivo_entrada = input("Ingrese el nombre del archivo de entrada: ")
    # nombre_archivo_salida = input("Ingrese el nombre del archivo de salida: ")
    nombre_archivo_entrada = "SGSSI-23.CB.06.txt"
    nombre_archivo_salida = "Output.txt"

    start = time.time()
    crear_fichero_salida(nombre_archivo_entrada, nombre_archivo_salida)
    end = time.time()

    print(f"Tiempo ejecución: {round(end - start, 6)}s")
