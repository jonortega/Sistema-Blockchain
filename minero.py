import hashlib
import time
import re


def imprimir_resultados(contador, ceros, sha256, valor_hex):
    print("===TIEMPO LIMITE (60s) ALCANZADO===")
    print(f"Iteraciones calculadas: {contador}")
    print(f"Hash con {ceros} ceros encontrado: {sha256}")
    print(f"Valor HEX con el que se ha obtenido: {valor_hex}")

def contar_ceros_iniciales(cadena):
    # Encuentra una o más ocurrencias de '0' al comienzo de la cadena
    match = re.match(r'^0+', cadena)
    if match:
        return len(match.group(0)) # Cantidad de ceros iniciales
    else:
        return 0

def calcular_sha256(nombre_fichero):
    sha256 = hashlib.sha256()
    with open(nombre_fichero, "rb") as archivo:
        while True:
            datos = archivo.read(65536)  # Leer 64KB a la vez
            if not datos:
                break
            sha256.update(datos)
    return sha256.hexdigest()

def escribir_nuevo_fichero_con_linea_final(nombre_fichero_entrada, nombre_fichero_salida, hex_adecuado):
    # Leer el contenido del fichero de entrada
    with open(nombre_fichero_entrada, "r") as entrada:
        contenido = entrada.read()

    with open(nombre_fichero_salida, "w") as salida:
        salida.write(contenido)
        
        # Agregar la línea adicional
        linea_adicional = f"{hex_adecuado}\tfe\t100\n"
        salida.write(linea_adicional)

def encontrar_hex_sha256(nombre_fichero_entrada, nombre_fichero_salida):
    valor_hex = "00000000" # Generar un valor hexadecimal inicial
    timeout = time.time() + 60 # Dentro de 60 segundos
    
    sha256_max_ceros = ""
    max_ceros = 0
    valor_hex_max_ceros = valor_hex

    contador = 0
    while True:
        if time.time() > timeout:
            # Escribir el valor hash con el que más ceros se obtien
            escribir_nuevo_fichero_con_linea_final(nombre_fichero_entrada, nombre_fichero_salida,valor_hex_max_ceros)
            imprimir_resultados(contador, max_ceros, sha256_max_ceros, valor_hex_max_ceros)
            break

        sha256 = calcular_sha256(nombre_fichero_salida)

        cantidad_ceros = contar_ceros_iniciales(sha256)
        if cantidad_ceros > max_ceros:
            max_ceros = cantidad_ceros
            sha256_max_ceros = sha256
            valor_hex_max_ceros = valor_hex
            print(f"(Ceros,Hex,SHA-256) = ({cantidad_ceros}, {valor_hex}, {sha256})")

        valor_hex = format(int(valor_hex, 16) + contador, "08x")

        escribir_nuevo_fichero_con_linea_final(nombre_fichero_entrada, nombre_fichero_salida, valor_hex)
        contador += 1

def crear_fichero_salida(nombre_fichero_entrada, nombre_fichero_salida):
    open(nombre_archivo_salida, "w") # Crear el fichero de salida vacio
    encontrar_hex_sha256(nombre_fichero_entrada, nombre_fichero_salida)

if __name__ == "__main__":
    nombre_archivo_entrada = input("Ingrese el nombre del archivo de entrada: ")
    nombre_archivo_salida = input("Ingrese el nombre del archivo de salida: ")
    # nombre_archivo_entrada = "SGSSI-23.CB.02.txt"
    # nombre_archivo_salida = "Output.txt"
    
    start = time.time()
    crear_fichero_salida(nombre_archivo_entrada, nombre_archivo_salida)
    end = time.time()
    
    print(f"Tiempo ejecucion: {round(end-start, 6)}s")
    print("Fichero de salida creado con exito.")
