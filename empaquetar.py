import zipfile
import os

#Empaqueta distintos archivos en un solo archivo (crea archivo_zip)
def empaquetar(archivo_zip, archivos, silencioso = False):
    with zipfile.ZipFile(archivo_zip, "w", zipfile.ZIP_DEFLATED) as z:
        for file in archivos:
            z.write(file)
    if silencioso == False:
        print("Se ha creado (o reemplazado) " + archivo_zip)

#Desempaqueta un archivo (antes empaquetado con la funcion anterior) y deja los archivos en una carpeta
def desempaquetar(archivo_zip, carpeta = "", silencioso = False):
    if carpeta == "":
        #carpeta = os.path.dirname(os.path.abspath(__file__))
        carpeta = os.getcwd()
    with zipfile.ZipFile(archivo_zip, "r") as z:
        z.extractall(carpeta)
    if silencioso == False:
        print("Archivos desempaquetados en:", carpeta)
