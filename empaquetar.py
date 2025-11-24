import zipfile
import os

#Empaqueta distintos archivos en un solo archivo (crea archivo_zip)
def empaquetar(archivo_zip, archivos, silencioso=False):
    with zipfile.ZipFile(archivo_zip, "w", zipfile.ZIP_DEFLATED) as z:
        for path in archivos:
            path = os.path.abspath(path)
            if os.path.isfile(path):
                z.write(path, arcname=os.path.basename(path))
            elif os.path.isdir(path):
                for root, dirs, files in os.walk(path):
                    for file in files:
                        full_path = os.path.join(root, file)
                        rel_path = os.path.relpath(full_path, os.path.dirname(path))
                        z.write(full_path, arcname=rel_path)
            else:
                print("Error: {path} no es un archivo ni carpeta")
    if not silencioso:
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
