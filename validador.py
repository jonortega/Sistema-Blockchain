import hashlib
import re
import os


def contar_ceros_iniciales(cadena):
    # Encuentra una o más ocurrencias de '0' al comienzo de la cadena
    match = re.match(r'^0+', cadena)
    if match:
        return len(match.group(0)) # Cantidad de ceros iniciales
    else:
        return 0

def calcular_sha256(nombre_archivo):
    sha256 = hashlib.sha256()

    try:
        with open(nombre_archivo, "rb") as archivo:
            while True:
                data = archivo.read(65536)  # Leer en bloques de 64 KB
                if not data:
                    break
                sha256.update(data)
        return sha256.hexdigest()
    except FileNotFoundError:
        return None

def comprobar_archivos(archivo_base, carpeta):
    
    if not os.path.exists(carpeta) or not os.path.isdir(carpeta):
        raise ValueError(f"La carpeta {carpeta} no existe o no es un directorio válido.")
    
    # Listar todos los archivos en la carpeta
    lista_archivos = os.listdir(carpeta)
    mejor_candidato = lista_archivos[0]
    num_ceros_max = 0

    try:
        cumplen = 0
        for archivo in lista_archivos:
            archivo = carpeta + "/" + archivo # Corregir la ruta relativa

            with open(archivo, "r") as file, open(archivo_base, "r") as base_file:
                contenido = file.read()
                contenido_base = base_file.read()

            resumen_sha256 = calcular_sha256(archivo)
            resumen_sha256_base = calcular_sha256(archivo_base)

            cumple_condicion = contenido.startswith(contenido_base) and \
                            bool(re.search(r'[0-9a-f]{8}\t[0-9a-f]{2}\t100$', contenido)) and \
                            bool(re.match(r'^0+', resumen_sha256))

            print(f"Fichero {archivo} cumple condición: {cumple_condicion}")
            
            if cumple_condicion:
                cumplen += 1
                num_ceros = contar_ceros_iniciales(resumen_sha256)

                print(f"Numero de ceros del Hash: {num_ceros}")

                if num_ceros > num_ceros_max:
                    num_ceros_max = num_ceros
                    mejor_candidato = archivo
        
        return mejor_candidato

    except FileNotFoundError:
        print("Al menos uno de los archivos no se encontró.")

if __name__ == "__main__":
    # archivo = input("Ingrese el nombre del archivo de texto: ")
    # carpeta = input("Ingrese el nombre de la carpeta de candidatos: ")
    archivo = "SGSSI-23.CB.04.txt"
    carpeta = "SGSSI-23.S.7.2.CB.04.Candidatos.Laboratorio"

    fichero_seleccionado = comprobar_archivos(archivo, carpeta)
    # print(f"Relación: {relacion}")
    print(f"Fichero seleccionado: {fichero_seleccionado}")
