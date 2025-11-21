import zipfile
import os

def empaquetar(archivo_zip, archivos):
    with zipfile.ZipFile(archivo_zip, "w", zipfile.ZIP_DEFLATED) as z:
        for file in archivos:
            z.write(file)
    print("Se ha creado (o reemplazado) " + archivo_zip)
    
def desempaquetar(archivo_zip, carpeta = ""):
    if carpeta == "":
        carpeta = os.path.dirname(os.path.abspath(__file__))
    with zipfile.ZipFile(archivo_zip, "r") as z:
        z.extractall(carpeta)
    print("Archivos desempaquetados en:", carpeta)
